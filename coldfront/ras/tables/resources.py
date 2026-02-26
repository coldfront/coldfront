# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.ras.models import Resource, ResourceType
from coldfront.tables import OrganizationalModelTable, PrimaryModelTable, columns


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
            "slug",
            "tags",
            "created",
            "last_updated",
            "actions",
        )
        default_columns = ("pk", "name", "color", "description")


class ResourceTable(PrimaryModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    resource_type = columns.ColoredLabelColumn(
        verbose_name=_("Type"),
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_("Status"),
    )
    tags = columns.TagColumn(
        url_name="ras:resource_list",
    )

    class Meta(PrimaryModelTable.Meta):
        model = Resource
        fields = (
            "pk",
            "id",
            "name",
            "slug",
            "resource_type",
            "status",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "resource_type", "status", "description")
