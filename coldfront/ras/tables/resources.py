# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.ras.models import Resource, ResourceType
from coldfront.tables import NestedGroupModelTable, OrganizationalModelTable, columns
from coldfront.tenancy.tables import TenancyColumnsMixin

from .template_code import ALLOCATIONTYPE_ATTRIBUTES


class ResourceTypeTable(OrganizationalModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    resource_count = columns.LinkedCountColumn(
        viewname="ras:resource_list",
        url_params={"resource_type_id": "pk"},
        verbose_name=_("Resource Count"),
    )
    color = columns.ColorColumn()

    attributes = columns.TemplateColumn(
        template_code=ALLOCATIONTYPE_ATTRIBUTES,
        accessor=tables.A("schema__properties"),
        orderable=False,
        verbose_name=_("Attributes"),
    )

    tags = columns.TagColumn(
        url_name="ras:resourcetype_list",
    )

    class Meta(OrganizationalModelTable.Meta):
        model = ResourceType
        fields = (
            "pk",
            "id",
            "name",
            "resource_count",
            "color",
            "description",
            "attributes",
            "slug",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "resource_count", "color", "attributes", "description")


class ResourceTable(TenancyColumnsMixin, NestedGroupModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    resource_type = columns.ColoredLabelColumn(
        verbose_name=_("Type"),
    )
    allocation_count = columns.LinkedCountColumn(
        viewname="ras:allocation_list",
        url_params={"resources": "pk"},
        verbose_name=_("Allocation Count"),
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_("Status"),
    )
    tags = columns.TagColumn(
        url_name="ras:resource_list",
    )

    class Meta(NestedGroupModelTable.Meta):
        model = Resource
        fields = (
            "pk",
            "id",
            "name",
            "slug",
            "parent",
            "resource_type",
            "status",
            "allocation_count",
            "description",
            "tags",
            "tenant",
            "tenant_group",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "resource_type", "status", "description", "allocation_count")
