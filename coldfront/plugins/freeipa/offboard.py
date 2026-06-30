# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Offboarding helpers: revoke a user's FreeIPA group memberships.

The signal path (``tasks.remove_user_group``) derives the ``.rw``/``.ro`` suffix from
the user's ProjectUser *role* and skips users whose role can no longer be resolved
(e.g. a departed user whose ProjectUser was hard-deleted). Those users therefore keep
their FreeIPA group membership — and their filesystem access — indefinitely.

This module offboards a user by *capture-and-attempt*, not by role: it derives the set
of managed groups from the user's allocations (the ``freeipa_group`` allocation attribute
value plus ``.rw``/``.ro`` — the same construction ``tasks.add_user_group`` uses), drops
any group the user still holds via another Active allocation, and removes the rest.

Both IPA-realm (internal) and AD-trust (external) members are supported; external
detection is by email domain via the ``FREEIPA_EXTERNAL_DOMAIN`` setting, and
``_remove_one`` attempts both member types so a misclassification is self-correcting.

The ``freeipa_group`` attribute value is treated as an opaque group base name; any
site-specific segments it carries (e.g. ``.e``/``.e.d`` markers for external/domain
groups) are preserved as-is, and ``.rw``/``.ro`` is appended. For AD-trust external
members there is no reverse "what groups is this user in" lookup, so we do not narrow by
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
GROUP_SUFFIXES = (".rw", ".ro")

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
    """The ``freeipa_group`` attribute values on an allocation (already carry .e/.e.d)."""
    return allocation.get_attribute_list(UNIX_GROUP_ATTRIBUTE_NAME)


def _suffixed(base_values):
    return {f"{value}{suffix}" for value in base_values for suffix in GROUP_SUFFIXES}


def managed_groups_for_user(user):
    """All ``<freeipa_group>.{rw,ro}`` groups derived from any allocation the user is on.

    Both suffixes are included because an offboarded user's role may no longer be
    resolvable, so we cannot know which they held; removing the other suffix is a no-op.
    """
    base_values = set()
    for au in AllocationUser.objects.filter(user=user).select_related("allocation"):
        base_values.update(_allocation_base_groups(au.allocation))
    return _suffixed(base_values)


def groups_to_keep(user, exclude_allocation_pk=None):
    """Groups the user still legitimately holds via an Active allocation elsewhere.

    Mirrors the cross-allocation safeguard in ``tasks.remove_user_group``: never remove a
    group the user retains through another live membership.
    """
    keep_allocations = Allocation.objects.filter(
        allocationuser__user=user,
        allocationuser__status__name=STATUS_ACTIVE,
        status__name=STATUS_ACTIVE,
        allocationattribute__allocation_attribute_type__name=UNIX_GROUP_ATTRIBUTE_NAME,
    ).distinct()
    if exclude_allocation_pk is not None:
        keep_allocations = keep_allocations.exclude(pk=exclude_allocation_pk)

    base_values = set()
    for a in keep_allocations:
        base_values.update(_allocation_base_groups(a))
    return _suffixed(base_values)


def plan_offboard(user, exclude_allocation_pk=None):
    """Compute ``(target_groups, kept_groups)`` for a user, applying the safeguard.

    ``target_groups`` is sorted. Targets are NOT narrowed by current membership (external
    members have no reverse lookup); removal of a non-membership is a no-op.
    """
    candidates = managed_groups_for_user(user)
    kept = groups_to_keep(user, exclude_allocation_pk=exclude_allocation_pk)
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


def offboard_user_groups_task(user_pk):
    """django-q entry point: revoke one user's FreeIPA groups (execute mode).

    Enqueued from the ProjectUser-removal cascade so the FreeIPA work runs in the
    qcluster worker, not the web request. Never raises. The cross-allocation safeguard in
    ``plan_offboard`` keeps any group the user still holds via an Active allocation.
    """
    from django.contrib.auth.models import User

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        logger.warning("offboard_user_groups_task: user pk=%s no longer exists", user_pk)
        return
    try:
        targets, kept = plan_offboard(user)
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
