# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.text import slugify

from coldfront.legacy.allocation.models import Allocation as _Allocation
from coldfront.legacy.project.models import Project as _Project
from coldfront.legacy.resource.models import Resource as _Resource
from coldfront.legacy.resource.models import ResourceType as _ResourceType
from coldfront.ras.choices import AllocationStatusChoices, ProjectStatusChoices, ResourceStatusChoices
from coldfront.ras.models import Allocation, AllocationUser, Project, ProjectUser, Resource, ResourceType


def migrate_resources():
    for rt in _ResourceType.objects.all():
        ResourceType.objects.get_or_create(
            id=rt.id,
            name=rt.name,
            slug=slugify(rt.name),
            description=rt.description,
            created=rt.created,
            last_updated=rt.modified,
        )

    for r in _Resource.objects.all():
        status = ResourceStatusChoices.STATUS_ACTIVE if r.is_available else ResourceStatusChoices.STATUS_OFFLINE
        Resource.objects.get_or_create(
            id=r.id,
            name=r.name,
            slug=slugify(r.name),
            resource_type_id=r.resource_type_id,
            status=status,
            description=r.description,
            created=r.created,
            last_updated=r.modified,
        )


def migrate_projects():
    for p in _Project.objects.all():
        status = ProjectStatusChoices.STATUS_NEW
        if p.status.name == "Archived":
            status = ProjectStatusChoices.STATUS_ARCHIVED
        elif p.status.name == "Active":
            status = ProjectStatusChoices.STATUS_ACTIVE

        Project.objects.get_or_create(
            id=p.id,
            name=p.title,
            status=status,
            description=p.description,
            owner_id=p.pi_id,
            created=p.created,
            last_updated=p.modified,
        )

        for u in p.projectuser_set.filter(status__name="Active"):
            ProjectUser.objects.get_or_create(
                project_id=p.id,
                user_id=u.user.id,
                created=u.created,
                last_updated=u.modified,
            )


def migrate_allocations():
    for a in _Allocation.objects.all():
        status = AllocationStatusChoices.STATUS_NEW
        if a.status.name == "Active":
            status = AllocationStatusChoices.STATUS_ACTIVE
        elif a.status.name == "Denied":
            status = AllocationStatusChoices.STATUS_DENIED

        r = a.resources.first()
        resource = Resource.objects.get(pk=r.id)
        allocation, _ = Allocation.objects.get_or_create(
            id=a.id,
            project_id=a.project_id,
            start_date=a.start_date,
            end_date=a.end_date,
            justification=a.justification,
            description=a.description,
            status=status,
            resource=resource,
            owner_id=a.project.pi_id,
            created=a.created,
            last_updated=a.modified,
        )

        for u in a.allocationuser_set.filter(status__name="Active"):
            AllocationUser.objects.get_or_create(
                allocation_id=a.id,
                user_id=u.user.id,
                created=u.created,
                last_updated=u.modified,
            )


def migrate_all():
    migrate_resources()
    migrate_projects()
    migrate_allocations()
