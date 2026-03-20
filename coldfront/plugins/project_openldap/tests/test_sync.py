# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import random
import string
from unittest.mock import patch

from coldfront.core.project.models import Project, ProjectStatusChoice
from coldfront.core.test_helpers.factories import ProjectFactory, ProjectUserFactory, UserFactory
from coldfront.plugins.project_openldap.management.commands import project_openldap_sync
from coldfront.plugins.project_openldap import tasks

from . import ProjectOpenLdapTestCase


class SyncTest(ProjectOpenLdapTestCase):
    def setUp(self):
        ProjectOpenLdapTestCase._setUp(self)
        super().setUp()

    def _sync(self, project: Project, **kwargs):
        command = project_openldap_sync.Command()
        command.sync_check_project(project.project_code, sync=True, **kwargs)

    def test_create(self):
        project = ProjectFactory(status__name="Active")
        self.assertFalse(self._does_project_nonArchived_ou_exist(project))
        self._sync(project)
        self.assertTrue(self._does_project_nonArchived_ou_exist(project))

    def test_delete(self):
        with (
            patch.object(project_openldap_sync, "PROJECT_OPENLDAP_REMOVE_PROJECT", True),
            patch.object(project_openldap_sync, "PROJECT_OPENLDAP_ARCHIVE_OU", ""),
            patch.object(tasks, "PROJECT_OPENLDAP_ARCHIVE_OU", ""),
        ):
            project = ProjectFactory(status__name="Active")
            self.assertFalse(self._does_project_nonArchived_ou_exist(project))
            self.assertFalse(self._does_project_archived_ou_exist(project))
            self._sync(project)
            self.assertTrue(self._does_project_nonArchived_ou_exist(project))
            self.assertFalse(self._does_project_archived_ou_exist(project))
            project.status = ProjectStatusChoice.objects.get(name="Archived")
            project.save()
            self._sync(project)
            self.assertFalse(self._does_project_nonArchived_ou_exist(project))
            self.assertFalse(self._does_project_archived_ou_exist(project))

    def test_archive(self):
        project = ProjectFactory(status__name="Active")
        self.assertFalse(self._does_project_archived_ou_exist(project))
        self.assertFalse(self._does_project_nonArchived_ou_exist(project))
        self._sync(project)
        self.assertFalse(self._does_project_archived_ou_exist(project))
        self.assertTrue(self._does_project_nonArchived_ou_exist(project))
        project.status = ProjectStatusChoice.objects.get(name="Archived")
        project.save()
        self._sync(project, write_to_archive=False)
        self.assertFalse(self._does_project_archived_ou_exist(project))
        self.assertTrue(self._does_project_nonArchived_ou_exist(project))
        self._sync(project, write_to_archive=True)
        self.assertTrue(self._does_project_archived_ou_exist(project))
        self.assertFalse(self._does_project_nonArchived_ou_exist(project))

    def test_add_member_uid(self):
        project = ProjectFactory(status__name="Active")
        self._sync(project)
        user = UserFactory()
        self.assertFalse(self._is_user_in_project_nonArchived_posixGroup(user, project))
        ProjectUserFactory(project=project, user=user)
        project.save()
        self._sync(project)
        self.assertTrue(self._is_user_in_project_nonArchived_posixGroup(user, project))

    def test_remove_member_uid(self):
        project = ProjectFactory(status__name="Active")
        user = UserFactory()
        ProjectUserFactory(project=project, user=user)
        project.save()
        self._sync(project)  # first sync creates the group but does not add members
        self._sync(project)  # second sync adds members
        self.assertTrue(self._is_user_in_project_nonArchived_posixGroup(user, project))
        project.remove_user(user)
        project.save()
        self._sync(project)
        self.assertFalse(self._is_user_in_project_nonArchived_posixGroup(user, project))

    def test_update_posixGroup_description(self):
        title_after = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        project = ProjectFactory(status__name="Active")
        self._sync(project)
        description_before = self._get_entry_description(self._get_project_nonArchived_posixGroup_dn(project))
        title_before = project.title
        self.assertIn(title_before, description_before)
        self.assertNotIn(title_after, description_before)
        project.title = title_after
        project.save()
        # nothing happens when CLI arg missing
        self._sync(project, update_description=False)
        description_after = self._get_entry_description(self._get_project_nonArchived_posixGroup_dn(project))
        self.assertIn(title_before, description_after)
        self.assertNotIn(title_after, description_after)
        # now something happens
        self._sync(project, update_description=True)
        description_after = self._get_entry_description(self._get_project_nonArchived_posixGroup_dn(project))
        self.assertNotIn(title_before, description_after)
        self.assertIn(title_after, description_after)
