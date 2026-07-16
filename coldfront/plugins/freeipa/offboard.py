# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Offboarding helpers: revoke a user's FreeIPA group memberships.

``tasks.remove_user_group`` removes a user from their groups when their
``AllocationUser`` is set to ``Removed``, but it is only ever called as a side effect of
that status change. A user whose ``ProjectUser`` (and so, by the cascade, their
``AllocationUser``) is hard-deleted rather than status-flipped never goes through that
path, so they keep their FreeIPA group membership — and the access it grants —
indefinitely.

This module offboards a user by *capture-and-attempt* instead: it derives the set of
groups the user's allocations grant, drops any group the user still holds via another
Active allocation (the same cross-allocation safeguard as ``tasks.remove_user_group``),
and removes the rest.

By default a group is the literal ``freeipa_group`` allocation attribute value, exactly
as ``tasks.add_user_group``/``remove_user_group`` use it. Deployments where one
allocation attribute value maps to more than one actual FreeIPA group — for example a
role-based naming convention layered on top by a downstream plugin — can pass
``group_names_for_allocation`` to every public function here to override the mapping.

Both IPA-realm (internal) and AD-trust (external) members are supported; external
detection is by email domain via the optional ``FREEIPA_EXTERNAL_DOMAIN`` setting
(unset → every user is treated as internal), and ``_remove_one``/``_add_one`` attempt
both member types so a misclassification is self-correcting. For external members there
is no reverse "what groups is this user in" lookup, so targets are not narrowed by
current membership — we attempt ``group_remove_member`` on each candidate and treat *not
a member* / *group not found* as harmless no-ops. The API result is the authoritative
record for audit and backout.

This module deliberately has no import-time side effects and does NOT import
``coldfront.plugins.freeipa.tasks`` (which runs a semaphore read, a sleep and a possible
``sys.exit`` at import).
"""

import logging

from coldfront.core.allocation.models import Allocation, AllocationUser
from coldfront.core.utils.common import import_from_settings
from coldfront.plugins.freeipa.utils import (
    UNIX_GROUP_ATTRIBUTE_NAME,
    AlreadyMemberError,
    NotMemberError,
    check_ipa_group_error,
    ipa_bootstrap,
)

logger = logging.getLogger(__name__)

STATUS_ACTIVE = "Active"

# Email domain whose users join FreeIPA groups as AD-trust external members
# (``ipaexternalmember``). Empty (the default) means every user is treated as an
# internal IPA-realm member; ``_remove_one`` falls back to the other member type anyway.
FREEIPA_EXTERNAL_DOMAIN = import_from_settings("FREEIPA_EXTERNAL_DOMAIN", "")


def is_external_member(user):
    """True if the user joins FreeIPA groups as an AD-trust external member.

    AD-trust domain users are external members (``ipaexternalmember``); IPA-realm users
    are internal (``user=[...]``). See the FREEIPA_EXTERNAL_DOMAIN setting. Matches on the
    email domain (not a substring) so e.g. ``x@notexample.org`` is not misread; the
    attempt-both-modes fallback in ``_remove_one`` covers any residual mismatch.
    """
    email = (user.email or "").lower()
    return email.endswith("@" + FREEIPA_EXTERNAL_DOMAIN.lower())


def _allocation_base_groups(allocation):
    """Default ``group_names_for_allocation``: the raw ``freeipa_group`` attribute
    value(s) on an allocation, unchanged -- the same names ``tasks.add_user_group`` and
    ``tasks.remove_user_group`` use."""
    return allocation.get_attribute_list(UNIX_GROUP_ATTRIBUTE_NAME)


def managed_groups_for_user(user, *, group_names_for_allocation=None):
    """All FreeIPA groups derived from any allocation the user is on.

    ``group_names_for_allocation`` is called once per allocation and must return an
    iterable of group names; it defaults to the literal ``freeipa_group`` attribute
    value(s) (see ``_allocation_base_groups``). Override it for a deployment where one
    attribute value maps to more than one actual group.
    """
    if group_names_for_allocation is None:
        group_names_for_allocation = _allocation_base_groups
    names = set()
    for au in AllocationUser.objects.filter(user=user).select_related("allocation"):
        names.update(group_names_for_allocation(au.allocation))
    return names


def groups_to_keep(user, exclude_allocation_pk=None, *, group_names_for_allocation=None):
    """Groups the user still legitimately holds via an Active allocation elsewhere.

    Mirrors the cross-allocation safeguard in ``tasks.remove_user_group``: never remove a
    group the user retains through another live membership. See ``managed_groups_for_user``
    for ``group_names_for_allocation``.
    """
    if group_names_for_allocation is None:
        group_names_for_allocation = _allocation_base_groups
    keep_allocations = Allocation.objects.filter(
        allocationuser__user=user,
        allocationuser__status__name=STATUS_ACTIVE,
        status__name=STATUS_ACTIVE,
        allocationattribute__allocation_attribute_type__name=UNIX_GROUP_ATTRIBUTE_NAME,
    ).distinct()
    if exclude_allocation_pk is not None:
        keep_allocations = keep_allocations.exclude(pk=exclude_allocation_pk)

    names = set()
    for a in keep_allocations:
        names.update(group_names_for_allocation(a))
    return names


def plan_offboard(user, exclude_allocation_pk=None, *, group_names_for_allocation=None):
    """Compute ``(target_groups, kept_groups)`` for a user, applying the safeguard.

    ``target_groups`` is sorted. Targets are NOT narrowed by current membership (external
    members have no reverse lookup); removal of a non-membership is a no-op. See
    ``managed_groups_for_user`` for ``group_names_for_allocation``.
    """
    candidates = managed_groups_for_user(user, group_names_for_allocation=group_names_for_allocation)
    kept = groups_to_keep(
        user, exclude_allocation_pk=exclude_allocation_pk, group_names_for_allocation=group_names_for_allocation
    )
    return sorted(candidates - kept), kept


def _remove_one(group, username, external):
    """Remove a member, trying the other member type on NotMemberError.

    Returns 'external'/'internal' on success, 'not-member' if in neither, 'no-group' if
    the group does not exist. Raises on any other API error.
    """
    from ipalib import api, errors

    order = ("external", "internal") if external else ("internal", "external")
    for mode in order:
        try:
            if mode == "external":
                res = api.Command.group_remove_member(group, ipaexternalmember=(username,))
            else:
                res = api.Command.group_remove_member(group, user=[username])
            check_ipa_group_error(res)
            return mode
        except NotMemberError:
            continue
        except errors.NotFound:
            return "no-group"
    return "not-member"


def _add_one(group, username, external):
    """Re-add a member (backout). Returns 'external'/'internal', 'already-member', or
    'no-group'. Raises on any other API error."""
    from ipalib import api, errors

    try:
        if external:
            res = api.Command.group_add_member(group, ipaexternalmember=(username,))
        else:
            res = api.Command.group_add_member(group, user=[username])
        check_ipa_group_error(res)
        return "external" if external else "internal"
    except AlreadyMemberError:
        return "already-member"
    except errors.NotFound:
        return "no-group"


def remove_user_from_groups(user, groups, *, dry_run, bootstrap=True):
    """Remove ``user`` from each group. Returns a list of per-group result records.

    Never raises: a single group's API failure is recorded and the rest proceed. result
    is 'would-remove' | 'removed:<mode>' | 'not-member' | 'no-group' | 'error'.
    """
    external = is_external_member(user)
    records = []
    if not dry_run and bootstrap:
        ipa_bootstrap()

    for g in groups:
        rec = {"group": g, "action": "remove", "user": user.username, "external": external, "dry_run": dry_run}
        if dry_run:
            rec["result"] = "would-remove"
            records.append(rec)
            continue
        try:
            mode = _remove_one(g, user.username, external)
            rec["result"] = mode if mode in ("not-member", "no-group") else f"removed:{mode}"
            if mode not in ("not-member", "no-group"):
                logger.info("Removed %s from FreeIPA group %s (%s)", user.username, g, mode)
        except Exception as e:
            rec["result"] = "error"
            rec["error"] = str(e)
            logger.error("Failed removing %s from group %s: %s", user.username, g, e)
        records.append(rec)
    return records


def add_user_to_groups(user, groups, *, dry_run, external=None, bootstrap=True):
    """Re-add ``user`` to each group (backout of a removal). Mirrors remove semantics.

    ``external`` overrides the member-type heuristic — backout passes the mode the
    original removal actually used, so a fallback removal is reversed faithfully.
    """
    if external is None:
        external = is_external_member(user)
    records = []
    if not dry_run and bootstrap:
        ipa_bootstrap()

    for g in groups:
        rec = {"group": g, "action": "add", "user": user.username, "external": external, "dry_run": dry_run}
        if dry_run:
            rec["result"] = "would-add"
            records.append(rec)
            continue
        try:
            mode = _add_one(g, user.username, external)
            rec["result"] = mode if mode in ("already-member", "no-group") else f"added:{mode}"
            if mode not in ("already-member", "no-group"):
                logger.info("Re-added %s to FreeIPA group %s (%s)", user.username, g, mode)
        except Exception as e:
            rec["result"] = "error"
            rec["error"] = str(e)
            logger.error("Failed adding %s to group %s: %s", user.username, g, e)
        records.append(rec)
    return records


def offboard_user_groups_task(user_pk, *, group_names_for_allocation=None):
    """django-q entry point: revoke one user's FreeIPA groups (execute mode).

    Enqueued from the ProjectUser-removal cascade so the FreeIPA work runs in the
    qcluster worker, not the web request. Never raises. The cross-allocation safeguard in
    ``plan_offboard`` keeps any group the user still holds via an Active allocation. See
    ``managed_groups_for_user`` for ``group_names_for_allocation``.
    """
    from django.contrib.auth.models import User

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.warning("offboard_user_groups_task: user pk=%s no longer exists", user_pk)
        return
    try:
        targets, kept = plan_offboard(user, group_names_for_allocation=group_names_for_allocation)
        logger.info(
            "offboard_user_groups_task: %s — %d group(s) to revoke, %d kept (active elsewhere)",
            user.username,
            len(targets),
            len(kept),
        )
        if targets:
            remove_user_from_groups(user, targets, dry_run=False)
    except Exception as e:
        logger.error("offboard_user_groups_task failed for %s: %s", user.username, e)
