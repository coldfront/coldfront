# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.ras.models import Allocation, Project, Resource, ResourceType
from coldfront.ras.models.projects import ProjectUser
from coldfront.slurm.models import (
    SlurmAccount,
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmUser,
)
from coldfront.users.models import User


class SlurmAssociationLifecycleTest(TestCase):
    """Test the lifecycle callbacks in coldfront.slurm.listeners."""

    @classmethod
    def setUpTestData(cls):
        # Users
        cls.user1 = User.objects.create(username="Alice")
        cls.user2 = User.objects.create(username="Bob")
        cls.user3 = User.objects.create(username="Charlie")

        # Project with members
        cls.project = Project.objects.create(name="Research Lab", owner=cls.user1)

        ProjectUser.objects.create(project=cls.project, user=cls.user1)
        ProjectUser.objects.create(project=cls.project, user=cls.user2)

        # Slurm cluster and partition
        cls.cluster = SlurmCluster.objects.create(name="hpc01")
        cls.partition = SlurmPartition.objects.create(
            name="gpu",
            cluster=cls.cluster,
        )

        # Slurm account
        cls.slurm_account = SlurmAccount.objects.create(
            name="lab-acct",
            cluster=cls.cluster,
        )

        # Resource type for generic FK (non-slurm)
        cls.resource_type = ResourceType.objects.create(name="Generic Resource")

        # ContentType for slurm cluster
        cls.cluster_ct = ContentType.objects.get_for_model(SlurmCluster)
        cls.partition_ct = ContentType.objects.get_for_model(SlurmPartition)
        cls.resource_ct = ContentType.objects.get_for_model(Resource)

    def setUp(self):
        # Clear any previously registered callbacks before each test
        AllocationStatusFlow._target_callbacks = {}
        AllocationStatusFlow._transition_permission_callbacks = {}

        # Re-register the slurm lifecycle callbacks
        from coldfront.slurm.listeners import (
            can_activate_check,
            on_allocation_activated,
        )

        AllocationStatusFlow.register_target_callback(
            AllocationStatusChoices.STATUS_ACTIVE,
            on_allocation_activated,
        )

        AllocationStatusFlow.register_transition_permission_callback(
            "activate",
            can_activate_check,
        )

    def _create_allocation(self, resource, resource_ct):
        return Allocation.objects.create(
            justification="Need compute resources",
            project=self.project,
            owner=self.user1,
            resource_object_type=resource_ct,
            resource_object_id=resource.pk,
        )

    # ---------- Step 1: On allocation requested ----------

    def test_request_creates_slurm_association_for_cluster(self):
        """Requesting an allocation targeting a SlurmCluster should create a SlurmAssociation."""
        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()

        # A SlurmAssociation should exist for this allocation
        association = SlurmAssociation.objects.filter(allocation=allocation).first()
        self.assertIsNotNone(association)

    def test_request_creates_slurm_association_for_partition(self):
        """Requesting an allocation targeting a SlurmPartition should create a SlurmAssociation."""
        allocation = self._create_allocation(self.partition, self.partition_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()

        association = SlurmAssociation.objects.filter(allocation=allocation).first()
        self.assertIsNotNone(association)

    def test_request_does_not_create_duplicate_association(self):
        """Requesting twice should not create a second SlurmAssociation."""
        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()
        flow.request()  # second call — self-loop on STATUS_NEW

        associations = SlurmAssociation.objects.filter(allocation=allocation)
        self.assertEqual(associations.count(), 1)

    def test_request_ignores_non_slurm_resource(self):
        """Requesting an allocation targeting a non-slurm resource should not create a SlurmAssociation."""
        resource = Resource.objects.create(
            name="Generic Storage",
            slug="s-1",
            resource_type=self.resource_type,
        )
        allocation = self._create_allocation(resource, self.resource_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()

        self.assertFalse(SlurmAssociation.objects.filter(allocation=allocation).exists())

    # ---------- Step 2: On allocation activated ----------

    def test_activate_creates_slurm_user_for_each_project_user(self):
        """Activating an allocation should create a SlurmUser for each ProjectUser
        if one doesn't already exist."""
        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        # Request -> create SlurmAssociation
        flow = AllocationStatusFlow(allocation)
        flow.request()

        # Set the slurm_account on the association (simulates admin action)
        association = SlurmAssociation.objects.get(allocation=allocation)
        association.slurm_account = self.slurm_account
        association.save()

        # Approve -> Activate
        flow.approve()
        flow.activate()

        # SlurmUser records should exist for Alice and Bob
        alice_su = SlurmUser.objects.filter(user=self.user1, cluster=self.cluster).first()
        bob_su = SlurmUser.objects.filter(user=self.user2, cluster=self.cluster).first()
        self.assertIsNotNone(alice_su)
        self.assertIsNotNone(bob_su)
        self.assertEqual(alice_su.default_account, self.slurm_account)
        self.assertEqual(bob_su.default_account, self.slurm_account)

    def test_activate_does_not_modify_existing_slurm_user(self):
        """Activating should not modify an existing SlurmUser record."""
        # Create a SlurmUser manually with a different default account
        other_account = SlurmAccount.objects.create(
            name="other-acct",
            cluster=self.cluster,
        )
        SlurmUser.objects.create(
            user=self.user1,
            cluster=self.cluster,
            default_account=other_account,
        )

        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()

        association = SlurmAssociation.objects.get(allocation=allocation)
        association.slurm_account = self.slurm_account
        association.save()

        flow.approve()
        flow.activate()

        # Alice's existing SlurmUser should still point to other_account
        alice_su = SlurmUser.objects.get(user=self.user1, cluster=self.cluster)
        self.assertEqual(alice_su.default_account, other_account)

        # Bob's SlurmUser should be created with slurm_account
        bob_su = SlurmUser.objects.get(user=self.user2, cluster=self.cluster)
        self.assertEqual(bob_su.default_account, self.slurm_account)

    def test_activate_skips_when_no_slurm_account_set(self):
        """Activating should not create SlurmUser records if slurm_account is null.

        Note: bypasses permission callbacks because the condition check would
        otherwise block the activate transition."""
        AllocationStatusFlow._transition_permission_callbacks = {}

        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()
        # Do NOT set slurm_account — leave it null
        flow.approve()
        flow.activate()

        # No SlurmUser records should exist
        self.assertFalse(SlurmUser.objects.filter(cluster=self.cluster).exists())

    def test_activate_skips_when_no_slurm_association(self):
        """Activating should skip if no SlurmAssociation exists for the allocation.

        Note: bypasses permission callbacks because the condition check would
        otherwise block the activate transition."""
        AllocationStatusFlow._transition_permission_callbacks = {}

        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        # Bypass the request callback — go straight to approve/activate
        # (simulates an allocation created without the callback)
        flow = AllocationStatusFlow(allocation)
        # Manually set status to approved so we can activate
        allocation.status = AllocationStatusChoices.STATUS_APPROVED
        allocation.save()

        flow.activate()

        # No SlurmUser records should exist
        self.assertFalse(SlurmUser.objects.filter(cluster=self.cluster).exists())

    def test_activate_ignores_non_slurm_resource(self):
        """Activating a non-slurm allocation should not create SlurmUser records."""
        resource = Resource.objects.create(
            name="Generic Storage",
            slug="s-1",
            resource_type=self.resource_type,
        )
        allocation = self._create_allocation(resource, self.resource_ct)

        flow = AllocationStatusFlow(allocation)
        # Request (no SlurmAssociation created for non-slurm resource)
        flow.request()

        # Manually set to approved so we can activate
        allocation.status = AllocationStatusChoices.STATUS_APPROVED
        allocation.save()

        flow.activate()

        self.assertFalse(SlurmUser.objects.filter(cluster__isnull=False).exists())

    # ---------- Permission callback tests ----------

    def test_activate_blocked_when_no_slurm_account(self):
        """
        The permission callback should block activation when the SlurmAssociation
        has no slurm_account set.
        """
        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()  # creates SlurmAssociation without slurm_account
        flow.approve()  # moves to STATUS_APPROVED

        # can_proceed passes (source matches), but has_perm fails (permission
        # callback denies it)
        self.assertTrue(flow.activate.can_proceed())
        self.assertFalse(flow.activate.has_perm(self.user1))

    def test_activate_allowed_when_slurm_account_set(self):
        """
        The permission callback should allow activation when the SlurmAssociation
        has a slurm_account set.
        """
        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()

        # Set the slurm_account on the association
        association = SlurmAssociation.objects.get(allocation=allocation)
        association.slurm_account = self.slurm_account
        association.save()

        flow.approve()

        self.assertTrue(flow.activate.can_proceed())
        self.assertTrue(flow.activate.has_perm(self.user1))

    def test_activate_allowed_for_non_slurm_allocation(self):
        """
        The permission callback should allow activation for non-slurm allocations
        (no SlurmAssociation exists — no restriction).
        """
        resource = Resource.objects.create(
            name="Generic Storage",
            slug="s-1",
            resource_type=self.resource_type,
        )
        allocation = self._create_allocation(resource, self.resource_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()  # no SlurmAssociation created for non-slurm
        flow.approve()

        self.assertTrue(flow.activate.can_proceed())
        self.assertTrue(flow.activate.has_perm(self.user1))

    def test_activate_blocked_when_no_registered_permission_callback(self):
        """
        If no permission callback is registered, can_activate should return True
        and the transition should be allowed.
        """
        # Clear permission callbacks for this test
        AllocationStatusFlow._transition_permission_callbacks = {}

        allocation = self._create_allocation(self.cluster, self.cluster_ct)

        flow = AllocationStatusFlow(allocation)
        flow.request()  # creates SlurmAssociation without slurm_account
        flow.approve()

        # With no permission callbacks registered, has_perm should pass
        # (can_activate returns True since _check_permission_callbacks finds nothing)
        self.assertTrue(flow.activate.can_proceed())
        self.assertTrue(flow.activate.has_perm(self.user1))
