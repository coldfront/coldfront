# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase

from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.ras.models import (
    Allocation,
    Project,
    Resource,
    ResourceType,
)
from coldfront.users.models import User


class AllocationStatusFlowTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="User1")
        project = Project.objects.create(name="Project 1", owner=user)
        resource_type = ResourceType.objects.create(name="Cluster")
        resource = Resource.objects.create(name="Resource 1", slug="r-1", resource_type=resource_type)
        Allocation.objects.create(
            justification="Need resources 1",
            project=project,
            owner=user,
            resource=resource,
        )

    def test_allocation_status_flow(self):
        allocation = Allocation.objects.first()
        flow = AllocationStatusFlow(allocation)

        flow.request()
        self.assertEqual(allocation.status, AllocationStatusChoices.STATUS_NEW)

        flow.approve()
        self.assertEqual(allocation.status, AllocationStatusChoices.STATUS_APPROVED)

        self.assertEqual(
            [
                (transition.target, transition.slug)
                for transition in AllocationStatusFlow.status.get_outgoing_transitions(allocation.status)
            ],
            [(AllocationStatusChoices.STATUS_ACTIVE, "activate")],
        )

        flow.activate()
        self.assertEqual(allocation.status, AllocationStatusChoices.STATUS_ACTIVE)

        self.assertEqual(
            [
                (transition.target, transition.slug)
                for transition in AllocationStatusFlow.status.get_outgoing_transitions(allocation.status)
            ],
            [
                (AllocationStatusChoices.STATUS_EXPIRED, "expire"),
                (AllocationStatusChoices.STATUS_RENEW, "renew"),
                (AllocationStatusChoices.STATUS_REVOKED, "revoke"),
            ],
        )

        flow.expire()
        self.assertEqual(allocation.status, AllocationStatusChoices.STATUS_EXPIRED)

        self.assertEqual(
            [
                (transition.target, transition.slug)
                for transition in AllocationStatusFlow.status.get_outgoing_transitions(allocation.status)
            ],
            [(AllocationStatusChoices.STATUS_RENEW, "renew")],
        )
