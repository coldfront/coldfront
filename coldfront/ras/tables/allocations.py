# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.ras.models import Allocation, AllocationType
from coldfront.tables import OrganizationalModelTable, PrimaryModelTable, columns

from .template_code import ALLOCATION_RESOURCES, ALLOCATIONTYPE_ATTRIBUTES


class AllocationTable(PrimaryModelTable):
    code = tables.TemplateColumn(
        accessor=tables.A("id"),
        template_code="allocation-{{ value }}",
        linkify=True,
        verbose_name=_("ID"),
    )

    project = tables.Column(
        verbose_name=_("Project"),
        linkify=True,
    )
    owner = tables.Column(
        verbose_name=_("Owner"),
    )

    resources = tables.TemplateColumn(
        template_code=ALLOCATION_RESOURCES,
        verbose_name=_("Resources"),
    )

    start_date = columns.DateColumn(
        verbose_name=_("Start Date"),
    )

    end_date = columns.DateColumn(
        verbose_name=_("End Date"),
    )

    status = columns.ChoiceFieldColumn(
        verbose_name=_("Status"),
    )

    tags = columns.TagColumn(
        url_name="ras:resource_list",
    )

    class Meta(PrimaryModelTable.Meta):
        model = Allocation
        fields = (
            "pk",
            "id",
            "project",
            "owner",
            "resources",
            "status",
            "description",
            "justification",
            "tags",
            "start_date",
            "end_date",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "code", "resources", "owner", "project", "status", "start_date", "end_date", "tags")


class AllocationTypeTable(OrganizationalModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )

    allocation_count = columns.LinkedCountColumn(
        viewname="ras:allocation_list",
        url_params={"allocation_type_id": "pk"},
        verbose_name=_("Allocation Count"),
    )

    attributes = columns.TemplateColumn(
        template_code=ALLOCATIONTYPE_ATTRIBUTES,
        accessor=tables.A("schema__properties"),
        orderable=False,
        verbose_name=_("Attributes"),
    )

    tags = columns.TagColumn(
        url_name="ras:allocationtype_list",
    )

    class Meta(PrimaryModelTable.Meta):
        model = AllocationType
        fields = (
            "pk",
            "id",
            "name",
            "description",
            "attributes",
            "allocation_count",
            "tags",
            "created",
            "last_updated",
            "actions",
        )
        default_columns = ("name", "allocation_count", "description", "attributes")
