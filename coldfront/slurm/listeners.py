# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.slurm.models import (
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmUser,
)


def on_allocation_requested(allocation, *, source, target):
    """
    On allocation requested: create a SlurmAssociation record linking to the
    allocation if one doesn't already exist.

    Callback signature: callback(obj, *, source, target)
    where obj is the allocation instance.
    """
    resource = allocation.resource_object
    if resource is None:
        return
    if not isinstance(resource, (SlurmCluster, SlurmPartition)):
        return

    # Create a SlurmAssociation if one doesn't already exist
    if not SlurmAssociation.objects.filter(allocation=allocation).exists():
        SlurmAssociation.objects.create(allocation=allocation)


def on_allocation_activated(allocation, *, source, target):
    """
    On allocation activate: for each ProjectUser (allocation.project.users),
    if no SlurmUser exists for (user, cluster), create one with default_account
    set to the active allocation's slurm_account.

    Existing records are never modified by subsequent allocation activations,
    preserving the original default.
    """
    resource = allocation.resource_object
    if resource is None:
        return
    if not isinstance(resource, (SlurmCluster, SlurmPartition)):
        return

    # Determine the cluster
    if isinstance(resource, SlurmCluster):
        cluster = resource
    else:
        cluster = resource.cluster

    # Get the slurm_account from the allocation's SlurmAssociation
    try:
        association = SlurmAssociation.objects.get(allocation=allocation)
    except SlurmAssociation.DoesNotExist:
        return

    slurm_account = association.slurm_account
    if slurm_account is None:
        return  # no account set yet, nothing to do

    # For each ProjectUser, create SlurmUser if not exists
    for project_user in allocation.project.users.all():
        user = project_user.user
        # get_or_create: existing records are never modified
        SlurmUser.objects.get_or_create(
            user=user,
            cluster=cluster,
            defaults={"default_account": slurm_account},
        )


# Register callbacks with AllocationStatusFlow.
# These are called during _dispatch_target_callbacks in
# AllocationStatusFlow._on_success_transition after a transition succeeds.
AllocationStatusFlow.register_target_callback(
    AllocationStatusChoices.STATUS_NEW,
    on_allocation_requested,
)
AllocationStatusFlow.register_target_callback(
    AllocationStatusChoices.STATUS_ACTIVE,
    on_allocation_activated,
)
