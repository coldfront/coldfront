# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.utils.text import slugify

from coldfront.legacy.allocation.models import Allocation as _Allocation
from coldfront.legacy.project.models import Project as _Project
from coldfront.legacy.resource.models import Resource as _Resource
from coldfront.legacy.resource.models import ResourceType as _ResourceType
from coldfront.ras.choices import AllocationStatusChoices, ProjectStatusChoices, ResourceStatusChoices
from coldfront.ras.models import Allocation, Project, Resource, ResourceType


def migrate_resources(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    for rt in _ResourceType.objects.using(db_alias).all():
        ResourceType.objects.using(db_alias).get_or_create(
            id=rt.id,
            name=rt.name,
            slug=slugify(rt.name),
            description=rt.description,
            created=rt.created,
            last_updated=rt.modified,
        )

    for r in _Resource.objects.using(db_alias).all():
        status = ResourceStatusChoices.STATUS_ACTIVE if r.is_available else ResourceStatusChoices.STATUS_OFFLINE
        Resource.objects.using(db_alias).get_or_create(
            id=r.id,
            name=r.name,
            resource_type_id=r.resource_type_id,
            status=status,
            description=r.description,
            created=r.created,
            last_updated=r.modified,
        )


def migrate_projects(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    for p in _Project.objects.using(db_alias).all():
        status = ProjectStatusChoices.STATUS_NEW
        if p.status.name == "Archived":
            status = ProjectStatusChoices.STATUS_ARCHIVED
        elif p.status.name == "Active":
            status = ProjectStatusChoices.STATUS_ACTIVE

        Project.objects.using(db_alias).get_or_create(
            id=p.id,
            name=p.title,
            status=status,
            description=p.description,
            owner_id=p.pi_id,
            created=p.created,
            last_updated=p.modified,
        )


def migrate_allocations(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    for a in _Allocation.objects.using(db_alias).all():
        status = AllocationStatusChoices.STATUS_NEW
        if a.status.name == "Active":
            status = AllocationStatusChoices.STATUS_ACTIVE
        elif a.status.name == "Denied":
            status = AllocationStatusChoices.STATUS_DENIED

        allocation, _ = Allocation.objects.using(db_alias).get_or_create(
            id=a.id,
            project_id=a.project_id,
            start_date=a.start_date,
            end_date=a.end_date,
            justification=a.justification,
            description=a.description,
            status=status,
            owner_id=a.project.pi_id,
            created=a.created,
            last_updated=a.modified,
        )

        for r in a.resources.all():
            resource = Resource.objects.using(db_alias).get(pk=r.id)
            allocation.resources.add(resource)
