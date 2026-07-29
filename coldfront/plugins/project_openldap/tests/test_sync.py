# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.core.project.models import Project, ProjectStatusChoice
from coldfront.core.test_helpers.factories import (
    ProjectFactory,
    ProjectStatusChoiceFactory,
    ProjectUserFactory,
    UserFactory,
)
from coldfront.plugins.project_openldap.management.commands.project_openldap_sync import Command

from . import ProjectOpenLdapTestCase


class SyncTest(ProjectOpenLdapTestCase):
    project_code = "proj001"
    gid_start = 8000

    @classmethod
    def setUpTestData(cls):
        cls.pi = UserFactory(username="pi_user")
        cls.project = ProjectFactory(
            pi=cls.pi,
            title="A very descriptive project title",
            project_code=cls.project_code,
            institution="Example Institute",
            status=ProjectStatusChoiceFactory(name="Active"),
        )
        cls.project_member = UserFactory(username="member_user")
        cls.project_user = ProjectUserFactory(project=cls.project, user=cls.project_member)

    def setUp(self):
        ProjectOpenLdapTestCase._setUp(self, gid_start=self.gid_start)
        self.project_ou_dn = self._get_project_ou_dn(self.project_code)
        self.project_group_dn = self._get_project_group_dn(self.project_code)
        self.project_archived_ou_dn = self._get_project_archived_ou_dn(self.project_code)
        self.project_archived_group_dn = self._get_project_archived_group_dn(self.project_code)
        self.command = Command()
        super().setUp()

    def _add_project_to_active_ou(self, members=None, description="", gid=None):
        members = members or []
        gid = gid or self.project.pk + self.gid_start
        self.mock_connection.strategy.add_entry(
            self.project_ou_dn,
            {"objectClass": ["top", "organizationalUnit"], "ou": [self.project_code]},
        )
        self.mock_connection.strategy.add_entry(
            self.project_group_dn,
            {
                "objectClass": ["top", "posixGroup"],
                "cn": [self.project_code],
                "gidNumber": [str(gid)],
                "description": [description],
                "memberUid": list(members),
            },
        )

    def test_sync_adds_missing_cf_member(self):
        """A CF member absent from LDAP is added when syncing."""
        self._add_project_to_active_ou()
        self.command.sync_check_project(self.project_code, sync=True)
        self.assertIn("member_user", self._get_project_member_uids(self.project_group_dn))

    def test_sync_removes_stale_ldap_member(self):
        """An LDAP member absent from CF is removed when syncing."""
        ProjectUserFactory._meta.model.objects.filter(pk=self.project_user.pk).delete()
        self._add_project_to_active_ou(members=["stale_user"])
        self.command.sync_check_project(self.project_code, sync=True)
        self.assertNotIn("stale_user", self._get_project_member_uids(self.project_group_dn))

    def test_missing_active_project_created(self):
        """An Active project missing from LDAP is created when syncing."""
        self.command.sync_check_project(self.project_code, sync=True)
        self.assertTrue(self._entry_exists(self.project_group_dn, "posixGroup"))

    def test_sync_updates_description(self):
        """An outdated LDAP posixGroup description is updated when update_description is requested."""
        self._add_project_to_active_ou(members=["member_user"])
        self.command.sync_check_project(self.project_code, sync=True, update_description=True)
        self.assertIn("A very descriptive project title", self._get_project_description(self.project_group_dn))

    def test_archived_project_moved_to_archive_ou(self):
        """An Archived project present in the active OU is moved to the archive OU when syncing."""
        self._add_project_to_active_ou(members=["member_user"])
        archived_status = ProjectStatusChoice.objects.get(name="Archived")
        Project.objects.filter(pk=self.project.pk).update(status=archived_status)
        self.command.sync_check_project(self.project_code, sync=True, write_to_archive=True)
        self.assertTrue(self._entry_exists(self.project_archived_ou_dn, "organizationalUnit"))
