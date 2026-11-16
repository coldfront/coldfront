# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
from unittest.mock import patch

from django.test import TestCase, override_settings

from coldfront.core.allocation import tasks
from coldfront.core.test_helpers.factories import (
    AllocationAttributeFactory,
    AllocationAttributeTypeFactory,
    AllocationFactory,
    AllocationStatusChoiceFactory,
    AllocationUserFactory,
    AllocationUserStatusChoiceFactory,
    ProjectFactory,
    ProjectUserFactory,
    ResourceAttributeFactory,
    ResourceAttributeTypeFactory,
    ResourceFactory,
    UserFactory,
)

BASE_URL = "https://coldfront.example.org"


@override_settings(ROOT_URLCONF="coldfront.core.test_helpers.base_path_urls")
@patch("coldfront.core.utils.mail.CENTER_BASE_URL", BASE_URL)
@patch("coldfront.core.allocation.tasks.send_email_template")
class AllocationTaskLinkTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.project = ProjectFactory()
        ProjectUserFactory(project=cls.project, user=cls.user)
        cls.resource = ResourceFactory()
        cls.project_url = f"{BASE_URL}/coldfront/project/{cls.project.pk}/"

    def create_allocation(self, status, end_date, user_status="Active"):
        allocation = AllocationFactory(
            project=self.project,
            status=AllocationStatusChoiceFactory(name=status),
            end_date=end_date,
        )
        allocation.resources.add(self.resource)
        AllocationUserFactory(
            allocation=allocation,
            user=self.user,
            status=AllocationUserStatusChoiceFactory(name=user_status),
        )
        return allocation

    def sent_context(self, mock_send, template_name):
        contexts = [call.args[2] for call in mock_send.call_args_list if call.args[1] == template_name]
        self.assertEqual(len(contexts), 1)
        return contexts[0]

    @patch("coldfront.core.allocation.tasks.EMAIL_ALLOCATION_EXPIRING_NOTIFICATION_DAYS", [7])
    def test_expiring_links_include_base_path(self, mock_send):
        end_date = datetime.date.today() + datetime.timedelta(days=7)
        allocation = self.create_allocation("Active", end_date)

        tasks.send_expiry_emails()

        context = self.sent_context(mock_send, "email/allocation_expiring.txt")
        project_url, renew_url, _ = context["expiration_dict"][7][0]
        self.assertEqual(project_url, self.project_url)
        self.assertEqual(renew_url, f"{BASE_URL}/coldfront/allocation/{allocation.pk}/renew")

    @patch("coldfront.core.allocation.tasks.EMAIL_ALLOCATION_EXPIRING_NOTIFICATION_DAYS", [7])
    def test_expiring_unpaid_links_to_allocation_detail(self, mock_send):
        end_date = datetime.date.today() + datetime.timedelta(days=7)
        allocation = self.create_allocation("Payment Pending", end_date)

        tasks.send_expiry_emails()

        context = self.sent_context(mock_send, "email/allocation_expiring.txt")
        _, renew_url, _ = context["expiration_dict"][7][0]
        self.assertEqual(renew_url, f"{BASE_URL}/coldfront/allocation/{allocation.pk}/")

    @patch("coldfront.core.allocation.tasks.EMAIL_ADMINS_ON_ALLOCATION_EXPIRE", True)
    def test_expired_links_include_base_path(self, mock_send):
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        allocation = self.create_allocation("Expired", end_date)
        AllocationAttributeFactory(
            allocation=allocation,
            allocation_attribute_type=AllocationAttributeTypeFactory(name="EXPIRE NOTIFICATION"),
            value="Yes",
        )

        tasks.send_expiry_emails()

        context = self.sent_context(mock_send, "email/allocation_expired.txt")
        self.assertEqual(context["project_dict"][self.project.title][0], self.project_url)
        self.assertEqual(
            context["allocation_dict"][self.project_url],
            [{f"{BASE_URL}/coldfront/allocation/{allocation.pk}/renew": self.resource.name}],
        )
        admin_context = self.sent_context(mock_send, "email/admin_allocation_expired.txt")
        self.assertEqual(
            admin_context["allocation_dict"][self.project_url],
            [{f"{BASE_URL}/coldfront/allocation/{allocation.pk}/": self.resource.name}],
        )

    def add_eula(self):
        ResourceAttributeFactory(
            resource=self.resource,
            resource_attribute_type=ResourceAttributeTypeFactory(name="eula"),
            value="Terms of use",
        )
        return self.create_allocation("Active", datetime.date.today(), user_status="PendingEULA")

    @patch("coldfront.core.allocation.tasks.ALLOCATION_EULA_ENABLE", True)
    def test_eula_reminder_link_includes_base_path(self, mock_send):
        allocation = self.add_eula()

        tasks.send_eula_reminders()

        context = self.sent_context(mock_send, "email/allocation_eula_reminder.txt")
        self.assertEqual(context["url"], f"{BASE_URL}/coldfront/allocation/{allocation.pk}/review-eula")

    @patch("coldfront.core.allocation.tasks.ALLOCATION_EULA_ENABLE", False)
    def test_eula_reminder_skipped_when_eula_disabled(self, mock_send):
        self.add_eula()

        tasks.send_eula_reminders()

        mock_send.assert_not_called()
