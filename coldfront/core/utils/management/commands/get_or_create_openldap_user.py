# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import argparse
from datetime import UTC, datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from ldap3 import SUBTREE, Connection, Server
from ldap3.core.exceptions import LDAPException
from ldap3.core.results import (
    RESULT_NO_SUCH_ATTRIBUTE,
    RESULT_NO_SUCH_OBJECT,
    RESULT_SUCCESS,
)

from coldfront.core.user.models import User

# This script uses the same settings as LDAP_USER_SEARCH_X as its assumed thats where users will come from
AUTH_LDAP_USER_SEARCH_BASE = settings.AUTH_LDAP_USER_SEARCH_BASE
LDAP_USER_SEARCH_BIND_DN = settings.LDAP_USER_SEARCH_BIND_DN
LDAP_USER_SEARCH_BIND_PASSWORD = settings.LDAP_USER_SEARCH_BIND_PASSWORD
LDAP_USER_SEARCH_SERVER_URI = settings.LDAP_USER_SEARCH_SERVER_URI
LDAP_USER_SEARCH_USE_SSL = settings.LDAP_USER_SEARCH_USE_SSL

DISCARD_LOCAL_USERS_SET = {
    "coldfront",
}

# Note: SASL not provided currently
tls = None

server = Server(
    LDAP_USER_SEARCH_SERVER_URI,
    use_ssl=LDAP_USER_SEARCH_USE_SSL,
    connect_timeout=2.5,
    tls=tls,
)


def non_empty_string(value: str) -> str:
    if not value.strip():
        raise argparse.ArgumentTypeError("argument cannot be empty or whitespace")
    return value


def change_user_pi(in_username, dry: bool, is_pi: bool):

    try:
        user = User.objects.get(username=in_username)
        if not user.userprofile.is_pi and is_pi:
            if dry:
                print(f"{in_username} was not granted PI status - dry mode is on!")
            else:
                user.userprofile.is_pi = True
                user.save()
        elif user.userprofile.is_pi and not is_pi:
            if dry:
                print(f"{in_username} was not revoked of PI status - dry mode is on!")
            else:
                user.userprofile.is_pi = False
                user.save()
    except User.DoesNotExist:
        print(
            f"{in_username} not found but was expected in Coldfront database to be able to change PI status to: {is_pi}"
        )


def print_users(is_pis):
    users = User.objects.filter(userprofile__is_pi=is_pis)
    for user in users:
        if user.username not in DISCARD_LOCAL_USERS_SET:
            print(f"{user.username}: {user.get_full_name()} ({user.email})")


def ldapsearch_get_all_uids(debug_mode, days_ago=0, input_username=None):
    """
    * Get all users (via posixAccount or input_username/uid) from AUTH_LDAP_USER_SEARCH_BASE using ldapsearch
    * raises `LDAPException` if the `ldap3.Connection` cannot be established or if the `ldap3.Result` code is nonzero
    """
    conn = Connection(
        server,
        LDAP_USER_SEARCH_BIND_DN,
        LDAP_USER_SEARCH_BIND_PASSWORD,
        auto_bind=True,
        read_only=True,
    )

    if input_username:
        final_search_filter = f"(&(uid={input_username}))"
    else:
        # calculate the timestamp for X days ago in UTC
        days_ago_ts = datetime.now(UTC) - timedelta(days_ago)
        # format to Generalized Time: YYYYMMDDhhmmssZ
        # Example output: 20261020113245Z
        ldap_timestamp = days_ago_ts.strftime("%Y%m%d%H%M%SZ")

        final_search_filter = f"(&(objectClass=posixAccount)(createTimestamp>={ldap_timestamp}))"

    if debug_mode:
        if input_username:
            print(f"SEARCHING FOR OPENLDAP USERNAME == {input_username}")
        else:
            print(f"SEARCHING FOR OPENLDAP USERS THAT HAVE createTimestamp>={ldap_timestamp} - USING days={days_ago}")
        print("-----")

    try:
        conn.search(
            search_base=AUTH_LDAP_USER_SEARCH_BASE,
            search_filter=final_search_filter,
            search_scope=SUBTREE,
            attributes=["cn", "uid", "mail", "givenName", "sn", "createTimestamp"],
        )

        entries = conn.entries.copy()
    finally:
        conn.unbind()
    if conn.result["result"] not in [
        RESULT_SUCCESS,
        RESULT_NO_SUCH_OBJECT,
        RESULT_NO_SUCH_ATTRIBUTE,
    ]:
        raise LDAPException(conn.result)
    return entries


def get_all_user_difference(debug_mode, ldapsearch_results, discard_users_set):

    FINAL_DISCARD_LOCAL_USERS_SET = DISCARD_LOCAL_USERS_SET.union(discard_users_set)

    usernames_set = set(User.objects.values_list("username", flat=True)) - FINAL_DISCARD_LOCAL_USERS_SET

    usernames_ldap_set = {entry.uid.value for entry in ldapsearch_results if entry.uid}

    if debug_mode:
        print("ALL DJANGO USER")
        print(usernames_set)
        print("OPENLDAP USERS (TO COMPARE)")
        print(usernames_ldap_set)

    # get DIFFERENCE of two sets
    diff_set = set(usernames_ldap_set - usernames_set)
    return diff_set


class Command(BaseCommand):
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--username",
            type=non_empty_string,
            help="The username of the target OpenLDAP user to sync into Coldfront",
        )
        group.add_argument(
            "--days",
            type=int,
            help="Number of days to consider for createTimestamp (e.g., 7 for a week). Helps stay inside OpenLDAP sizelimit.",
        )
        group.add_argument(
            "--print_pis",
            action="store_true",
            help="Print all PIs (not standard users)",
        )
        group.add_argument(
            "--print_users",
            action="store_true",
            help="Print all users (not PIs)",
        )
        parser.add_argument(
            "--dry",
            action="store_true",
            help="Enable dry mode - don't save user objects to Coldfront database",
        )
        parser.add_argument(
            "--DEBUG",
            action="store_true",
            help="Enable DEBUG mode",
        )
        parser.add_argument(
            "--discard_users",
            nargs="*",
            default=[],
            help="Discard additional users (space-separated list). Coldfront named user is automatically discarded.",
        )
        parser.add_argument(
            "--make_pi",
            action="store_true",
            help="Also grant supplied --username PI status",
        )
        parser.add_argument(
            "--revoke_pi",
            action="store_true",
            help="Also revoke supplied --username PI status",
        )

    def handle(self, *args, **options):
        # Perform cross-argument validation inside handle()
        if options["make_pi"] and not options["username"]:
            raise CommandError("--username is required when --make_pi is used.")
        if options["revoke_pi"] and not options["username"]:
            raise CommandError("--username is required when --revoke_pi is used.")
        if options["make_pi"] and options["revoke_pi"]:
            raise CommandError("--make_pi cant be used with --revoke_pi")

        print_all_pis = options["print_pis"]
        print_all_users = options["print_users"]
        if print_all_pis:
            print_users(is_pis=True)
            return
        if print_all_users:
            print_users(is_pis=False)
            return

        input_username = options["username"]
        make_user_pi = options["make_pi"]
        revoke_user_pi = options["revoke_pi"]
        debug_mode = options["DEBUG"]
        days_ago = options["days"]
        dry_mode = options["dry"]
        discard_users_set = set(options["discard_users"])

        results = ldapsearch_get_all_uids(debug_mode, days_ago, input_username)

        diff_result = get_all_user_difference(debug_mode, results, discard_users_set)

        if len(diff_result) == 0:
            if debug_mode:
                print("NO USERS TO ADD")
            # no users to add, but PI status is to be changed...
            if input_username and make_user_pi:
                if debug_mode:
                    print(f"Ensure {input_username} has PI status granted")
                change_user_pi(input_username, dry_mode, is_pi=True)
            if input_username and revoke_user_pi:
                if debug_mode:
                    print(f"Ensure {input_username} has PI status REVOKED")
                change_user_pi(input_username, dry_mode, is_pi=False)

        if len(diff_result) > 0:
            print("EXPECTING TO ADD:")
            print(diff_result)

            for entry in results:
                username = str(entry.uid[0]) if entry.uid else None
                if username not in diff_result:
                    continue

                try:
                    user_to_get = entry["uid"].value
                    user = User.objects.get(username=user_to_get)

                except User.DoesNotExist:
                    print(f"{user_to_get} is going to be added to Coldfront database.")
                    user = User(
                        username=entry["cn"].value,
                        email=entry["mail"].value,
                        first_name=entry["givenName"].value,
                        last_name=entry["sn"].value,
                    )
                    if dry_mode:
                        print(f"{user_to_get} was not saved - dry mode is on!")
                    else:
                        user.save()
