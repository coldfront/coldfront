# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from unittest.mock import patch

from coldfront.core.test_helpers.factories import (
    ProjectFactory,
    ProjectStatusChoiceFactory,
    ProjectUserFactory,
    UserFactory,
)
from coldfront.plugins.project_openldap import tasks

from . import ProjectOpenLdapTestCase


class TasksTest(ProjectOpenLdapTestCase):
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
        self._setUp(self.gid_start)
        self.project_ou_dn = self._get_project_ou_dn(self.project_code)
        self.project_group_dn = self._get_project_group_dn(self.project_code)
        self.project_archived_ou_dn = self._get_project_archived_ou_dn(self.project_code)
        self.project_archived_group_dn = self._get_project_archived_group_dn(self.project_code)
        super().setUp()

    def test_openldap_add_project(self):
        tasks.add_project(self.project)
        self.assertTrue(self._entry_exists(self.project_ou_dn, "organizationalUnit"))
        self.assertTrue(self._entry_exists(self.project_group_dn, "posixGroup"))
        self.assertIn(self.project.pi.username, self._get_project_member_uids(self.project_group_dn))
        self.assertEqual(self._get_project_gid_number(self.project_group_dn), self.project.pk + self.gid_start)

    def test_openldap_remove_project(self):
        tasks.add_project(self.project)
        with (
            patch.object(tasks, "PROJECT_OPENLDAP_REMOVE_PROJECT", True),
            patch.object(tasks, "PROJECT_OPENLDAP_ARCHIVE_OU", ""),
        ):
            tasks.remove_project(self.project)
        self.assertFalse(self._entry_exists(self.project_group_dn, "posixGroup"))
        self.assertFalse(self._entry_exists(self.project_ou_dn, "organizationalUnit"))

    def test_openldap_archive_project(self):
        tasks.add_project(self.project)
        with (
            patch.object(tasks, "PROJECT_OPENLDAP_REMOVE_PROJECT", False),
            patch.object(tasks, "PROJECT_OPENLDAP_ARCHIVE_OU", self.archived_projects_ou),
            patch("coldfront.plugins.project_openldap.utils.PROJECT_OPENLDAP_ARCHIVE_OU", self.archived_projects_ou),
        ):
            tasks.remove_project(self.project)
        self.assertFalse(self._entry_exists(self.project_ou_dn, "organizationalUnit"))
        self.assertTrue(self._entry_exists(self.project_archived_ou_dn, "organizationalUnit"))

    def test_openldap_update_project(self):
        tasks.add_project(self.project)
        self.project.title = "Updated title for LDAP description"
        tasks.update_project(self.project)
        description = self._get_project_description(self.project_group_dn)
        self.assertIn("Updated title for LDAP description", description)

    def test_openldap_add_user_project(self):
        tasks.add_project(self.project)
        tasks.add_user_project(self.project_user.pk)
        member_uids = self._get_project_member_uids(self.project_group_dn)
        self.assertIn(self.project.pi.username, member_uids)
        self.assertIn(self.project_member.username, member_uids)

    def test_openldap_remove_user_project(self):
        tasks.add_project(self.project)
        tasks.add_user_project(self.project_user.pk)
        tasks.remove_user_project(self.project_user.pk)
        member_uids = self._get_project_member_uids(self.project_group_dn)
        self.assertIn(self.project.pi.username, member_uids)
        self.assertNotIn(self.project_member.username, member_uids)
