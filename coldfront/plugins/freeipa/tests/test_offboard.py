# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Unit tests for freeipa/offboard.py."""

import sys
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# IPA stubs — ipalib and freeipa utils both require IPA to be installed and
# configured. Stub them out so tests run without an IPA enrolment.
# ---------------------------------------------------------------------------


# Concrete exception classes so except-clauses in offboard.py work correctly.
class _NotMemberError(Exception):
    pass


class _AlreadyMemberError(Exception):
    pass


_ipa_stub = MagicMock()
_ipa_errors_stub = MagicMock()
# Make errors.NotFound a concrete exception so offboard._remove_one can catch it.
_ipa_errors_stub.NotFound = type("NotFound", (Exception,), {})
# `from ipalib import errors` resolves the attribute on the ipalib module, so point
# it at the same stub that carries the concrete NotFound class.
_ipa_stub.errors = _ipa_errors_stub
sys.modules.setdefault("ipalib", _ipa_stub)
sys.modules.setdefault("ipalib.errors", _ipa_errors_stub)


def _fake_check_ipa_group_error(res):
    """Faithful re-implementation of utils.check_ipa_group_error.

    Mirrors the real logic (utils.py) so the real ``_remove_one``/``_add_one`` exception
    paths are exercised rather than stubbed away. Raises the same _NotMemberError /
    _AlreadyMemberError that offboard.py imports from this stubbed utils module.
    """
    if not res:
        raise ValueError("Missing FreeIPA response")
    if res["completed"] == 1:
        return
    try:
        err_msg = res["failed"]["member"]["user"][0][1]
    except (KeyError, IndexError):
        try:
            err_msg = res["failed"]["member"]["group"][0][1]
        except (KeyError, IndexError):
            err_msg = None
    if err_msg == "This entry is already a member":
        raise _AlreadyMemberError(err_msg)
    if err_msg == "This entry is not a member":
        raise _NotMemberError(err_msg)
    raise Exception(err_msg)


# freeipa utils reads required FreeIPA Django settings at import time.  Stub
# the module so tests can load offboard.py in any environment.
_utils_stub = MagicMock()
_utils_stub.FREEIPA_EXTERNAL_DOMAIN = "example.org"
_utils_stub.UNIX_GROUP_ATTRIBUTE_NAME = "freeipa_group"
_utils_stub.AlreadyMemberError = _AlreadyMemberError
_utils_stub.NotMemberError = _NotMemberError
_utils_stub.check_ipa_group_error = _fake_check_ipa_group_error
_utils_stub.ipa_bootstrap = MagicMock()
sys.modules["coldfront.plugins.freeipa.utils"] = _utils_stub


def _completed():
    return {"completed": 1}


def _not_member():
    return {"completed": 0, "failed": {"member": {"user": [["x", "This entry is not a member"]]}}}


def _already_member():
    return {"completed": 0, "failed": {"member": {"user": [["x", "This entry is already a member"]]}}}


from django.test import TestCase  # noqa: E402

from coldfront.core.test_helpers.factories import (  # noqa: E402
    AAttributeTypeFactory,
    AllocationAttributeFactory,
    AllocationAttributeTypeFactory,
    AllocationFactory,
    AllocationStatusChoiceFactory,
    AllocationUserFactory,
    AllocationUserStatusChoiceFactory,
    ProjectFactory,
    UserFactory,
)

FREEIPA_GROUP_ATTR = "freeipa_group"


def _make_allocation(user, group_value, alloc_status="Active", au_status="Active"):
    """Create an allocation with a freeipa_group attribute and an AllocationUser."""
    status = AllocationStatusChoiceFactory(name=alloc_status)
    alloc = AllocationFactory(
        project=ProjectFactory(),
        status=status,
    )
    attr_type = AAttributeTypeFactory(name="Text")
    alloc_attr_type = AllocationAttributeTypeFactory(
        name=FREEIPA_GROUP_ATTR,
        attribute_type=attr_type,
    )
    AllocationAttributeFactory(
        allocation_attribute_type=alloc_attr_type,
        allocation=alloc,
        value=group_value,
    )
    au_status_obj = AllocationUserStatusChoiceFactory(name=au_status)
    AllocationUserFactory(allocation=alloc, user=user, status=au_status_obj)
    return alloc


class IsExternalMemberTest(TestCase):
    def setUp(self):
        self.patcher = patch(
            "coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN",
            "example.org",
        )
        self.patcher.start()
        from coldfront.plugins.freeipa import offboard

        self.offboard = offboard

    def tearDown(self):
        self.patcher.stop()

    def test_external_email(self):
        u = UserFactory(email="alice@example.org")
        self.assertTrue(self.offboard.is_external_member(u))

    def test_internal_email(self):
        u = UserFactory(email="bob@ipa.example.org")
        self.assertFalse(self.offboard.is_external_member(u))

    def test_subdomain_not_misread(self):
        u = UserFactory(email="carol@notexample.org")
        self.assertFalse(self.offboard.is_external_member(u))

    def test_blank_email(self):
        u = UserFactory(email="")
        self.assertFalse(self.offboard.is_external_member(u))


class ManagedGroupsForUserTest(TestCase):
    def test_no_allocations(self):
        from coldfront.plugins.freeipa.offboard import managed_groups_for_user

        u = UserFactory()
        self.assertEqual(managed_groups_for_user(u), set())

    def test_groups_from_single_allocation(self):
        from coldfront.plugins.freeipa.offboard import managed_groups_for_user

        u = UserFactory()
        _make_allocation(u, "proj1.e.d")
        result = managed_groups_for_user(u)
        self.assertEqual(result, {"proj1.e.d.rw", "proj1.e.d.ro"})

    def test_dedup_across_allocations(self):
        from coldfront.plugins.freeipa.offboard import managed_groups_for_user

        u = UserFactory()
        _make_allocation(u, "proj1.e.d")
        _make_allocation(u, "proj1.e.d")  # same base, second allocation
        result = managed_groups_for_user(u)
        self.assertEqual(result, {"proj1.e.d.rw", "proj1.e.d.ro"})

    def test_multiple_allocations(self):
        from coldfront.plugins.freeipa.offboard import managed_groups_for_user

        u = UserFactory()
        _make_allocation(u, "projA.e.d")
        _make_allocation(u, "projB.e")
        result = managed_groups_for_user(u)
        self.assertIn("projA.e.d.rw", result)
        self.assertIn("projB.e.ro", result)


class GroupsToKeepTest(TestCase):
    def test_active_allocation_elsewhere_kept(self):
        from coldfront.plugins.freeipa.offboard import groups_to_keep

        u = UserFactory()
        _make_allocation(u, "live.e.d", alloc_status="Active", au_status="Active")
        result = groups_to_keep(u)
        self.assertIn("live.e.d.rw", result)
        self.assertIn("live.e.d.ro", result)

    def test_removed_au_not_kept(self):
        from coldfront.plugins.freeipa.offboard import groups_to_keep

        u = UserFactory()
        _make_allocation(u, "gone.e.d", alloc_status="Active", au_status="Removed")
        result = groups_to_keep(u)
        self.assertNotIn("gone.e.d.rw", result)

    def test_inactive_allocation_not_kept(self):
        from coldfront.plugins.freeipa.offboard import groups_to_keep

        u = UserFactory()
        _make_allocation(u, "expired.e.d", alloc_status="Expired", au_status="Active")
        result = groups_to_keep(u)
        self.assertNotIn("expired.e.d.rw", result)

    def test_exclude_allocation_pk(self):
        from coldfront.plugins.freeipa.offboard import groups_to_keep

        u = UserFactory()
        alloc = _make_allocation(u, "proj.e.d", alloc_status="Active", au_status="Active")
        result = groups_to_keep(u, exclude_allocation_pk=alloc.pk)
        self.assertNotIn("proj.e.d.rw", result)


class PlanOffboardTest(TestCase):
    def test_all_targets_when_no_active_elsewhere(self):
        from coldfront.plugins.freeipa.offboard import plan_offboard

        u = UserFactory()
        _make_allocation(u, "proj.e.d", alloc_status="Active", au_status="Removed")
        targets, kept = plan_offboard(u)
        self.assertIn("proj.e.d.rw", targets)
        self.assertEqual(len(kept), 0)

    def test_kept_excludes_from_targets(self):
        from coldfront.plugins.freeipa.offboard import plan_offboard

        u = UserFactory()
        _make_allocation(u, "proj.e.d", alloc_status="Active", au_status="Active")
        targets, kept = plan_offboard(u)
        self.assertNotIn("proj.e.d.rw", targets)
        self.assertIn("proj.e.d.rw", kept)

    def test_targets_sorted(self):
        from coldfront.plugins.freeipa.offboard import plan_offboard

        u = UserFactory()
        _make_allocation(u, "beta.e", alloc_status="Active", au_status="Removed")
        _make_allocation(u, "alpha.e", alloc_status="Active", au_status="Removed")
        targets, _ = plan_offboard(u)
        self.assertEqual(targets, sorted(targets))


class RemoveUserFromGroupsTest(TestCase):
    def test_dry_run_no_api_call(self):
        from coldfront.plugins.freeipa.offboard import remove_user_from_groups

        u = UserFactory(username="alice")
        with patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap") as mock_boot:
            records = remove_user_from_groups(u, ["proj.e.d.rw"], dry_run=True)
        mock_boot.assert_not_called()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["result"], "would-remove")
        self.assertEqual(records[0]["action"], "remove")
        self.assertEqual(records[0]["user"], "alice")

    def test_execute_success_external(self):
        from coldfront.plugins.freeipa.offboard import remove_user_from_groups

        u = UserFactory(username="alice", email="alice@example.org")
        with (
            patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap"),
            patch("coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN", "example.org"),
            patch("coldfront.plugins.freeipa.offboard._remove_one", return_value="external") as mock_rm,
        ):
            records = remove_user_from_groups(u, ["proj.e.d.rw"], dry_run=False)
        mock_rm.assert_called_once_with("proj.e.d.rw", "alice", True)
        self.assertEqual(records[0]["result"], "removed:external")

    def test_execute_not_member_noop(self):
        from coldfront.plugins.freeipa.offboard import remove_user_from_groups

        u = UserFactory(username="bob", email="bob@ipa.example.org")
        with (
            patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap"),
            patch("coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN", "example.org"),
            patch("coldfront.plugins.freeipa.offboard._remove_one", return_value="not-member"),
        ):
            records = remove_user_from_groups(u, ["proj.e.d.rw"], dry_run=False)
        self.assertEqual(records[0]["result"], "not-member")

    def test_execute_no_group_noop(self):
        from coldfront.plugins.freeipa.offboard import remove_user_from_groups

        u = UserFactory(username="carol", email="carol@ipa.example.org")
        with (
            patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap"),
            patch("coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN", "example.org"),
            patch("coldfront.plugins.freeipa.offboard._remove_one", return_value="no-group"),
        ):
            records = remove_user_from_groups(u, ["ghost.rw"], dry_run=False)
        self.assertEqual(records[0]["result"], "no-group")

    def test_execute_api_error_never_raises(self):
        from coldfront.plugins.freeipa.offboard import remove_user_from_groups

        u = UserFactory(username="dave", email="dave@ipa.example.org")
        with (
            patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap"),
            patch("coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN", "example.org"),
            patch("coldfront.plugins.freeipa.offboard._remove_one", side_effect=RuntimeError("timeout")),
        ):
            records = remove_user_from_groups(u, ["proj.rw"], dry_run=False)
        self.assertEqual(records[0]["result"], "error")
        self.assertIn("timeout", records[0]["error"])


class AddUserToGroupsTest(TestCase):
    def test_dry_run(self):
        from coldfront.plugins.freeipa.offboard import add_user_to_groups

        u = UserFactory(username="alice")
        records = add_user_to_groups(u, ["proj.rw"], dry_run=True)
        self.assertEqual(records[0]["result"], "would-add")

    def test_already_member(self):
        from coldfront.plugins.freeipa.offboard import add_user_to_groups

        u = UserFactory(username="bob", email="bob@ipa.example.org")
        with (
            patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap"),
            patch("coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN", "example.org"),
            patch("coldfront.plugins.freeipa.offboard._add_one", return_value="already-member"),
        ):
            records = add_user_to_groups(u, ["proj.rw"], dry_run=False)
        self.assertEqual(records[0]["result"], "already-member")

    def test_success_external_override(self):
        from coldfront.plugins.freeipa.offboard import add_user_to_groups

        u = UserFactory(username="carol", email="carol@ipa.example.org")
        with (
            patch("coldfront.plugins.freeipa.offboard.ipa_bootstrap"),
            patch("coldfront.plugins.freeipa.offboard.FREEIPA_EXTERNAL_DOMAIN", "example.org"),
            patch("coldfront.plugins.freeipa.offboard._add_one", return_value="external") as mock_add,
        ):
            records = add_user_to_groups(u, ["proj.rw"], dry_run=False, external=True)
        mock_add.assert_called_once_with("proj.rw", "carol", True)
        self.assertEqual(records[0]["result"], "added:external")


class OffboardUserGroupsTaskTest(TestCase):
    def test_user_not_found_no_raise(self):
        from coldfront.plugins.freeipa.offboard import offboard_user_groups_task

        with patch("coldfront.plugins.freeipa.offboard.plan_offboard") as mock_plan:
            offboard_user_groups_task(user_pk=999999)
        mock_plan.assert_not_called()

    def test_normal_path_calls_remove(self):
        from coldfront.plugins.freeipa.offboard import offboard_user_groups_task

        u = UserFactory()
        with (
            patch(
                "coldfront.plugins.freeipa.offboard.plan_offboard", return_value=(["proj.e.d.rw"], set())
            ) as mock_plan,
            patch("coldfront.plugins.freeipa.offboard.remove_user_from_groups") as mock_rm,
        ):
            offboard_user_groups_task(user_pk=u.pk)
        mock_plan.assert_called_once_with(u)
        mock_rm.assert_called_once_with(u, ["proj.e.d.rw"], dry_run=False)

    def test_empty_targets_no_remove_call(self):
        from coldfront.plugins.freeipa.offboard import offboard_user_groups_task

        u = UserFactory()
        with (
            patch("coldfront.plugins.freeipa.offboard.plan_offboard", return_value=([], {"proj.e.d.rw"})),
            patch("coldfront.plugins.freeipa.offboard.remove_user_from_groups") as mock_rm,
        ):
            offboard_user_groups_task(user_pk=u.pk)
        mock_rm.assert_not_called()

    def test_exception_never_raises(self):
        from coldfront.plugins.freeipa.offboard import offboard_user_groups_task

        u = UserFactory()
        with patch("coldfront.plugins.freeipa.offboard.plan_offboard", side_effect=RuntimeError("oops")):
            offboard_user_groups_task(user_pk=u.pk)  # must not raise


class RemoveOneRealTest(TestCase):
    """Exercise the REAL _remove_one — only the ipalib api boundary is mocked.

    Covers the FreeIPA call construction, the external->internal fallback, the
    check_ipa_group_error exception handling, and the errors.NotFound path.
    """

    def setUp(self):
        from coldfront.plugins.freeipa import offboard

        self.offboard = offboard
        self.cmd = MagicMock()
        _ipa_stub.api.Command = self.cmd
        self.addCleanup(lambda: setattr(_ipa_stub.api, "Command", MagicMock()))

    def test_external_success(self):
        self.cmd.group_remove_member.return_value = _completed()
        result = self.offboard._remove_one("grp.rw", "alice", external=True)
        self.assertEqual(result, "external")
        self.cmd.group_remove_member.assert_called_once_with("grp.rw", ipaexternalmember=("alice",))

    def test_internal_success(self):
        self.cmd.group_remove_member.return_value = _completed()
        result = self.offboard._remove_one("grp.rw", "bob", external=False)
        self.assertEqual(result, "internal")
        self.cmd.group_remove_member.assert_called_once_with("grp.rw", user=["bob"])

    def test_external_falls_back_to_internal(self):
        # External attempt reports not-a-member; internal attempt succeeds.
        self.cmd.group_remove_member.side_effect = [_not_member(), _completed()]
        result = self.offboard._remove_one("grp.rw", "alice", external=True)
        self.assertEqual(result, "internal")
        self.assertEqual(self.cmd.group_remove_member.call_count, 2)

    def test_not_member_in_either_mode(self):
        self.cmd.group_remove_member.side_effect = [_not_member(), _not_member()]
        result = self.offboard._remove_one("grp.rw", "alice", external=True)
        self.assertEqual(result, "not-member")

    def test_no_group(self):
        self.cmd.group_remove_member.side_effect = _ipa_errors_stub.NotFound("no such group")
        result = self.offboard._remove_one("ghost.rw", "alice", external=True)
        self.assertEqual(result, "no-group")


class AddOneRealTest(TestCase):
    """Exercise the REAL _add_one — only the ipalib api boundary is mocked."""

    def setUp(self):
        from coldfront.plugins.freeipa import offboard

        self.offboard = offboard
        self.cmd = MagicMock()
        _ipa_stub.api.Command = self.cmd
        self.addCleanup(lambda: setattr(_ipa_stub.api, "Command", MagicMock()))

    def test_external_success(self):
        self.cmd.group_add_member.return_value = _completed()
        result = self.offboard._add_one("grp.rw", "alice", external=True)
        self.assertEqual(result, "external")
        self.cmd.group_add_member.assert_called_once_with("grp.rw", ipaexternalmember=("alice",))

    def test_internal_success(self):
        self.cmd.group_add_member.return_value = _completed()
        result = self.offboard._add_one("grp.rw", "bob", external=False)
        self.assertEqual(result, "internal")
        self.cmd.group_add_member.assert_called_once_with("grp.rw", user=["bob"])

    def test_already_member(self):
        self.cmd.group_add_member.return_value = _already_member()
        result = self.offboard._add_one("grp.rw", "alice", external=True)
        self.assertEqual(result, "already-member")

    def test_no_group(self):
        self.cmd.group_add_member.side_effect = _ipa_errors_stub.NotFound("no such group")
        result = self.offboard._add_one("ghost.rw", "alice", external=True)
        self.assertEqual(result, "no-group")
