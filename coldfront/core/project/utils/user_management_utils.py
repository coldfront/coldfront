# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.core.allocation.models import AllocationUser, AllocationUserStatusChoice
from coldfront.core.allocation.signals import allocation_activate_user, allocation_remove_user
from coldfront.core.project.models import ProjectUser, ProjectUserStatusChoice
from coldfront.core.project.signals import project_activate_user, project_remove_user


def add_user_to_project(project_obj, user_obj, role_choice, send_signals=True, obj_class=None):
    """Utility function to get or create a ProjectUser. Updates role and status if already exists.
    sends project_activate_user signal if send_signals is True."""
    project_user_active_status_choice = ProjectUserStatusChoice.objects.get(name="Active")
    created = False
    if project_obj.projectuser_set.filter(user=user_obj).exists():
        project_user_obj = project_obj.projectuser_set.get(user=user_obj)
        project_user_obj.role = role_choice
        project_user_obj.status = project_user_active_status_choice
        project_user_obj.save()
    else:
        project_user_obj = ProjectUser.objects.create(
            user=user_obj,
            project=project_obj,
            role=role_choice,
            status=project_user_active_status_choice,
        )
        created = True

    if send_signals:
        if obj_class is not None:
            project_activate_user.send(sender=obj_class, project_user_pk=project_user_obj.pk)
        else:
            project_activate_user.send(project_user_pk=project_user_obj.pk)

    return project_user_obj, created


def remove_user_from_project(project_obj, user_obj, send_signals=True, obj_class=None):
    """Utility function to remove a user from a project. fires project_remove_user
    signal and allocation_remove_user for each allocation in the project if send_signals is True."""
    # do not allow removing the PI
    if project_obj.pi == user_obj:
        return False
    project_user_removed_status_choice = ProjectUserStatusChoice.objects.get(name="Removed")
    if project_obj.projectuser_set.filter(user=user_obj, status__name="Active").exists():
        project_user_obj = project_obj.projectuser_set.get(user=user_obj)
        project_user_obj.status = project_user_removed_status_choice
        project_user_obj.save()

        if send_signals:
            if obj_class is not None:
                project_remove_user.send(sender=obj_class, project_user_pk=project_user_obj.pk)
            else:
                project_remove_user.send(project_user_pk=project_user_obj.pk)

        # get allocations to remove users from
        allocations_to_remove_user_from = project_obj.allocation_set.filter(
            status__name__in=["Active", "New", "Renewal Requested"]
        )
        for allocation in allocations_to_remove_user_from:
            remove_user_from_allocation(allocation, user_obj, send_signals, obj_class)
        return True
    return False


def remove_user_from_allocation(allocation, user_obj, send_signals=True, obj_class=None):
    """Utility function to remove an Active user from an allocation. fires allocation_remove_user
    signal if send_signals is True."""
    allocation_user_removed_status_choice = AllocationUserStatusChoice.objects.get(name="Removed")
    for allocation_user_obj in allocation.allocationuser_set.filter(user=user_obj, status__name__in=["Active"]):
        allocation_user_obj.status = allocation_user_removed_status_choice
        allocation_user_obj.save()

        if send_signals:
            if obj_class is not None:
                allocation_remove_user.send(sender=obj_class, allocation_user_pk=allocation_user_obj.pk)
            else:
                allocation_remove_user.send(allocation_user_pk=allocation_user_obj.pk)


def add_user_to_allocation(
    allocation, user_obj, user_status_choice=None, send_signals_on_activate=True, obj_class=None
):
    """Utility function to remove a user from a list of allocations. fires allocation_remove_user
    signal for each allocation in the project if send_signals is True."""
    active_status_choice = AllocationUserStatusChoice.objects.get(name="Active")
    user_status_choice = user_status_choice or active_status_choice

    activated = False
    if AllocationUser.objects.filter(allocation=allocation, user=user_obj).exists():
        allocation_user_obj = AllocationUser.objects.get(allocation=allocation, user=user_obj)
        # status is changing to user_status_choice
        if allocation_user_obj.status != user_status_choice:
            allocation_user_obj.status = user_status_choice
            allocation_user_obj.save()
            # new status is Active
            if user_status_choice == active_status_choice:
                activated = True
    else:
        allocation_user_obj = AllocationUser.objects.create(
            allocation=allocation, user=user_obj, status=user_status_choice
        )
        # creating a new allocation user with Active status is implicit activation
        if user_status_choice == active_status_choice:
            activated = True

    if send_signals_on_activate and activated:
        if obj_class is not None:
            allocation_activate_user.send(sender=obj_class, allocation_user_pk=allocation_user_obj.pk)
        else:
            allocation_activate_user.send(allocation_user_pk=allocation_user_obj.pk)
