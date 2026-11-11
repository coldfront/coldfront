# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import UTC, datetime, timedelta

from django.core.management.base import BaseCommand
from ldap3 import SUBTREE, Connection, Server
from ldap3.core.exceptions import LDAPException
from ldap3.core.results import (
    RESULT_NO_SUCH_ATTRIBUTE,
    RESULT_NO_SUCH_OBJECT,
    RESULT_SUCCESS,
)

from coldfront.core.user.models import User
from coldfront.core.utils.common import import_from_settings

# This script uses the same settings as LDAP_USER_SEARCH_X as its assumed thats where users will come from
AUTH_LDAP_USER_SEARCH_BASE = import_from_settings("AUTH_LDAP_USER_SEARCH_BASE")
LDAP_USER_SEARCH_BIND_DN = import_from_settings("LDAP_USER_SEARCH_BIND_DN")
LDAP_USER_SEARCH_BIND_PASSWORD = import_from_settings("LDAP_USER_SEARCH_BIND_PASSWORD")
LDAP_USER_SEARCH_SERVER_URI = import_from_settings("LDAP_USER_SEARCH_SERVER_URI")
LDAP_USER_SEARCH_USE_SSL = import_from_settings("LDAP_USER_SEARCH_USE_SSL")

DISCARD_LOCAL_USERS = {
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


def ldapsearch_get_all_uids(days_ago, debug_mode, input_username=None):
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

    # calculate the timestamp for X days ago in UTC
    days_ago_ts = datetime.now(UTC) - timedelta(days_ago)

    # format to Generalized Time: YYYYMMDDhhmmssZ
    # Example output: 20261020113245Z
    ldap_timestamp = days_ago_ts.strftime("%Y%m%d%H%M%SZ")

    if debug_mode:
        print("-----")
        print(f"SEARCHING FOR OPENLDAP USERS THAT HAVE createTimestamp>={ldap_timestamp} - USING days={days_ago}")
        print("-----")

    final_search_filter = f"(&(objectClass=posixAccount)(createTimestamp>={ldap_timestamp}))"
    if input_username:
        final_search_filter = f"(&(uid={input_username})(createTimestamp>={ldap_timestamp}))"

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


def get_all_user_difference(ldapsearch_results, debug_mode):

    usernames_set = set(User.objects.values_list("username", flat=True)) - DISCARD_LOCAL_USERS

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
    help = "With no arguments supplied this management command will compare all openldap users with Coldfront django and register missing into the Coldfront database OR supply --username to register a single username in Coldfront database. --dry to run in dry mode and not write changes. --DEBUG to show output."

    def add_arguments(self, parser):
        # Username is a required argument
        parser.add_argument(
            "--username",
            type=str,
            help="The username of the target User to sync into Coldfront",
        )
        parser.add_argument(
            "--dry",
            action="store_true",
            help="Enable dry mode - dont save user objects to Coldfront database",
        )
        parser.add_argument("--DEBUG", action="store_true", help="Enable DEBUG mode")
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Number of days to consider for createTimestamp, default 7, a week. This helps limit results returned and to potentially stay inside an OpenLDAP sizelimit.",
        )

    def handle(self, *args, **options):

        input_username = False
        input_username = options["username"]
        debug_mode = False
        debug_mode = options["DEBUG"]

        days_ago = options["days"]

        if not input_username:
            results = ldapsearch_get_all_uids(days_ago, debug_mode)
        else:
            results = ldapsearch_get_all_uids(days_ago, debug_mode, input_username)

        diff_result = get_all_user_difference(results, debug_mode)

        if len(diff_result) == 0 and debug_mode:
            print("NO USERS TO ADD")

        if len(diff_result) > 0:
            print("EXPECTING TO ADD:")
            print(diff_result)

            for entry in results:
                username = str(entry.uid[0]) if entry.uid else None
                if username in diff_result:
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
                        if options["dry"]:
                            print(f"{user_to_get} was not saved - dry mode is on!")
                        if not options["dry"]:
                            user.save()
                        else:
                            print("No changes made - dry mode on")
