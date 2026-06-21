# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db.models.signals import post_save
from django.dispatch import receiver

from coldfront.flows import register_target_callback, register_transition_permission_callback
from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.ras.models import Allocation
from coldfront.slurm.models import (
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmUser,
)


@receiver(post_save, sender=Allocation)
def on_allocation_created(instance, created, **kwargs):
    """
    When an allocation is created: create a SlurmAssociation record linking to the
    allocation if one doesn't already exist.
    """
    if not created:
        return

    resource = instance.resource_object
    if resource is None:
        return
    if not isinstance(resource, (SlurmCluster, SlurmPartition)):
        return

    # Create a SlurmAssociation if one doesn't already exist
    if not SlurmAssociation.objects.filter(allocation=instance).exists():
        SlurmAssociation.objects.create(allocation=instance)


@register_target_callback(AllocationStatusFlow, AllocationStatusChoices.STATUS_ACTIVE)
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


@register_transition_permission_callback(AllocationStatusFlow, "activate")
def can_activate_check(allocation, user):
    """
    Permission callback for the "activate" transition.

    Blocks activation if the allocation has a SlurmAssociation that still
    has no slurm_account set.  Non-slurm allocations are always allowed.
    """
    resource = allocation.resource_object
    if not isinstance(resource, (SlurmCluster, SlurmPartition)):
        return True

    association = SlurmAssociation.objects.filter(allocation=allocation).first()
    if association is None:
        return False

    return association.slurm_account is not None
