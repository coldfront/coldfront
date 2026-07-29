# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from ldap3 import BASE, MOCK_SYNC, Connection, Server

from coldfront.plugins.project_openldap import tasks


class ProjectOpenLdapTestCase(TestCase):
    projects_ou: str
    archived_projects_ou: str
    mock_server: Server
    mock_connection: Connection

    @classmethod
    def setUpClass(cls):
        call_command("add_default_project_choices")
        super(ProjectOpenLdapTestCase, cls).setUpClass()

    def _setUp(self, gid_start):
        root_ou = "dc=example,dc=edu"
        bind_username = "bind_username"
        bind_dn = f"cn={bind_username},{root_ou}"
        bind_password = "bind_password"
        self.projects_ou = f"ou=projects,{root_ou}"
        self.archived_projects_ou = f"ou=archive,{root_ou}"
        self.mock_server = Server("mock_ldap")
        self.mock_connection = Connection(
            self.mock_server, user=bind_dn, password=bind_password, client_strategy=MOCK_SYNC
        )
        self.mock_connection.strategy.add_entry(root_ou, {"objectClass": ["top", "domain"], "dc": ["example"]})
        self.mock_connection.strategy.add_entry(
            self.projects_ou, {"objectClass": ["top", "organizationalUnit"], "ou": ["projects"]}
        )
        self.mock_connection.strategy.add_entry(
            self.archived_projects_ou, {"objectClass": ["top", "organizationalUnit"], "ou": ["archive"]}
        )
        self.mock_connection.strategy.add_entry(
            bind_dn,
            {"objectClass": ["top", "person"], "cn": ["foo"], "sn": ["bar"], "userPassword": [bind_password]},
        )

        def openldap_connection_mock(_server_opt, _bind_user, _bind_password):
            self.mock_connection.bind()
            return self.mock_connection

        self.openldap_conn_patch = patch(
            "coldfront.plugins.project_openldap.utils.openldap_connection", side_effect=openldap_connection_mock
        )
        self.openldap_conn_patch.start()
        self.addCleanup(self.openldap_conn_patch.stop)
        self.tasks_constants_patch = patch.multiple(
            tasks,
            PROJECT_OPENLDAP_OU=self.projects_ou,
            PROJECT_OPENLDAP_ARCHIVE_OU=self.archived_projects_ou,
            PROJECT_OPENLDAP_GID_START=gid_start,
            PROJECT_OPENLDAP_REMOVE_PROJECT=True,
        )
        self.tasks_constants_patch.start()
        self.addCleanup(self.tasks_constants_patch.stop)
        self.utils_constants_patch = patch.multiple(
            "coldfront.plugins.project_openldap.utils",
            PROJECT_OPENLDAP_OU=self.projects_ou,
            PROJECT_OPENLDAP_ARCHIVE_OU=self.archived_projects_ou,
            PROJECT_OPENLDAP_BIND_USER=bind_dn,
            PROJECT_OPENLDAP_BIND_PASSWORD=bind_password,
            PROJECT_OPENLDAP_DESCRIPTION_TITLE_LENGTH=100,
        )
        self.utils_constants_patch.start()
        self.addCleanup(self.utils_constants_patch.stop)
        self.sync_constants_patch = patch.multiple(
            "coldfront.plugins.project_openldap.management.commands.project_openldap_sync",
            PROJECT_OPENLDAP_OU=self.projects_ou,
            PROJECT_OPENLDAP_ARCHIVE_OU=self.archived_projects_ou,
            PROJECT_OPENLDAP_GID_START=gid_start,
            PROJECT_OPENLDAP_REMOVE_PROJECT=True,
            PROJECT_OPENLDAP_EXCLUDE_USERS=[],
        )
        self.sync_constants_patch.start()
        self.addCleanup(self.sync_constants_patch.stop)

    def _entry_exists(self, dn, objectClass) -> bool:
        self.mock_connection.bind()
        try:
            return self.mock_connection.search(dn, f"(objectclass={objectClass})", search_scope=BASE)
        finally:
            self.mock_connection.unbind()

    def _get_project_attribute(self, dn: str, attribute: str):
        self.mock_connection.bind()
        try:
            self.mock_connection.search(dn, "(objectclass=posixGroup)", search_scope=BASE, attributes=[attribute])
            self.assertEqual(len(self.mock_connection.entries), 1)
            return self.mock_connection.entries[0][attribute]
        finally:
            self.mock_connection.unbind()

    def _get_project_member_uids(self, dn) -> set[str]:
        return set(self._get_project_attribute(dn, "memberUid"))

    def _get_project_description(self, dn) -> str:
        return str(self._get_project_attribute(dn, "description"))

    def _get_project_gid_number(self, dn) -> int:
        return int(str(self._get_project_attribute(dn, "gidNumber")))

    def _get_project_ou_dn(self, project_code):
        return f"ou={project_code},{self.projects_ou}"

    def _get_project_group_dn(self, project_code):
        return f"cn={project_code},ou={project_code},{self.projects_ou}"

    def _get_project_archived_ou_dn(self, project_code):
        return f"ou={project_code},{self.archived_projects_ou}"

    def _get_project_archived_group_dn(self, project_code):
        return f"cn={project_code},ou={project_code},{self.archived_projects_ou}"
