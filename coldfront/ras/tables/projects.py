# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.ras.models import Project
from coldfront.tables import OrganizationalModelTable, columns


class ProjectTable(OrganizationalModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    owner = tables.Column(
        linkify=True,
        verbose_name=_("Owner"),
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_("Status"),
    )
    tags = columns.TagColumn(
        url_name="ras:project_list",
    )

    class Meta(OrganizationalModelTable.Meta):
        model = Project
        fields = (
            "pk",
            "id",
            "name",
            "owner",
            "status",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "owner", "status", "description", "tags")
