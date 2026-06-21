# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from coldfront.flows import register_target_callback, register_transition_permission_callback
from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.ras.models import Allocation, ProjectUser
from coldfront.slurm.models import (
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmUser,
)


def _get_cluster_account_pairs(project):
    """
    Given a project, return a dict mapping SlurmCluster -> slurm_account
    (the first SlurmAccount from active allocations on that cluster).

    Only considers active (STATUS_ACTIVE) allocations whose resource_object
    is a SlurmCluster or SlurmPartition.
    """
    result = {}
    allocations = Allocation.objects.filter(
        project=project,
        status=AllocationStatusChoices.STATUS_ACTIVE,
    ).select_related(
        "resource_object_type",
    )
    for allocation in allocations:
        resource = allocation.resource_object
        if resource is None:
            continue
        if isinstance(resource, SlurmPartition):
            cluster = resource.cluster
        elif isinstance(resource, SlurmCluster):
            cluster = resource
        else:
            continue

        if cluster.pk in result:
            continue  # already have an account for this cluster

        try:
            association = SlurmAssociation.objects.get(allocation=allocation)
        except SlurmAssociation.DoesNotExist:
            continue

        if association.slurm_account is None:
            continue

        result[cluster.pk] = (cluster, association.slurm_account)

    return result


def _sync_slurm_users_for_user(user):
    """
    Reconcile SlurmUser records for a given user against all projects they
    belong to.

    For each cluster the user has access to (via an active slurm allocation
    on any project), ensure a SlurmUser exists with the correct default_account.
    For clusters the user no longer has access to, remove the SlurmUser record.
    """
    # Collect all cluster->account pairs across all projects this user belongs to
    cluster_account = {}  # cluster_pk -> (cluster, slurm_account)
    for pu in ProjectUser.objects.filter(user=user).select_related("project"):
        pairs = _get_cluster_account_pairs(pu.project)
        for pk, (cluster, account) in pairs.items():
            if pk not in cluster_account:
                cluster_account[pk] = (cluster, account)

    # Get all SlurmUser records for this user
    existing_users = {
        su.cluster.pk: su
        for su in SlurmUser.objects.filter(user=user).select_related("cluster")
    }

    # For each cluster the user has access to
    for pk, (cluster, slurm_account) in cluster_account.items():
        if pk in existing_users:
            # Update if the default_account changed
            su = existing_users[pk]
            if su.default_account != slurm_account:
                su.default_account = slurm_account
                su.save()
        else:
            # Create a new SlurmUser
            SlurmUser.objects.create(
                user=user,
                cluster=cluster,
                default_account=slurm_account,
            )

    # For clusters the user no longer has access to, remove the SlurmUser
    for pk, su in existing_users.items():
        if pk not in cluster_account:
            su.delete()


@receiver(post_save, sender=ProjectUser)
def on_project_user_saved(instance, created, **kwargs):
    """
    When a ProjectUser is created (or updated), ensure SlurmUser records
    exist for the user based on all active slurm allocations on the project.
    """
    if created:
        _sync_slurm_users_for_user(instance.user)


@receiver(post_delete, sender=ProjectUser)
def on_project_user_deleted(instance, **kwargs):
    """
    When a ProjectUser is deleted, reconcile SlurmUser records for the user
    against all remaining projects they belong to.
    """
    _sync_slurm_users_for_user(instance.user)


@receiver(post_save, sender=SlurmAssociation)
def on_slurm_association_saved(instance, **kwargs):
    """
    When a SlurmAssociation is saved, sync SlurmUser records for all project
    members if the linked allocation is active.

    This handles the case where an admin edits a SlurmAssociation and
    changes the slurm_account on an active allocation.  The underlying
    _sync_slurm_users_for_user already handles no-ops efficiently.
    """
    allocation = instance.allocation
    if allocation.status != AllocationStatusChoices.STATUS_ACTIVE:
        return  # only sync for active allocations

    resource = allocation.resource_object
    if resource is None:
        return
    if not isinstance(resource, (SlurmCluster, SlurmPartition)):
        return

    # Sync SlurmUser for each project member
    for project_user in allocation.project.users.all():
        _sync_slurm_users_for_user(project_user.user)


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
