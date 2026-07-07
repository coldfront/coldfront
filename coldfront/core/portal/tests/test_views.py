# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django.test import TestCase

from coldfront.core.test_helpers import utils
from coldfront.core.test_helpers.factories import UserFactory

logging.disable(logging.CRITICAL)


class PortalViewBaseTest(TestCase):
    """Base class for portal view tests."""

    @classmethod
    def setUpTestData(cls):
        """Test Data setup for all portal view tests."""
        pass


class CenterSummaryViewTest(PortalViewBaseTest):
    """Tests for center summary view"""

    @classmethod
    def setUpTestData(cls):
        """Set up users and project for testing"""
        cls.url = "/center-summary"
        super(PortalViewBaseTest, cls).setUpTestData()

    def test_centersummary_renders(self):
        response = self.client.get(self.url)
        utils.assert_response_success(self, response)
        self.assertContains(response, "Active Allocations and Users")
        self.assertContains(response, "Resources and Allocations Summary")
        self.assertNotContains(response, "We're having a bit of system trouble at the moment. Please check back soon!")


class NavbarPermissionTest(PortalViewBaseTest):
    """The staff navbar menu appears for permission holders without staff status"""

    def test_staff_menu_for_permission_holder(self):
        user = UserFactory(username="menu_perm_holder", is_staff=False, is_superuser=False)
        utils.page_does_not_contain_for_user(self, user, "/", 'id="navbar-admin"')
        user = utils.grant_user_permission(user, "allocation", "can_view_all_allocations")
        utils.page_contains_for_user(self, user, "/", 'id="navbar-admin"')
        # User Search requires staff status; permission holders must not see it
        utils.page_does_not_contain_for_user(self, user, "/", "User Search")

    def test_staff_menu_for_staff_user(self):
        staff_user = UserFactory(username="staff_menu_user", is_staff=True, is_superuser=False)
        utils.page_contains_for_user(self, staff_user, "/", 'id="navbar-admin"')
        utils.page_contains_for_user(self, staff_user, "/", "User Search")
