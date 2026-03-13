# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.ras.models import Project, ProjectUser
from coldfront.tables import OrganizationalModelTable, PrimaryModelTable, columns


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


class ProjectUserTable(PrimaryModelTable):
    user = tables.Column(
        linkify=("ras:projectuser", {"pk": tables.A("id")}),
        verbose_name=_("User"),
    )

    project = tables.Column(
        verbose_name=_("Project"),
        linkify=True,
    )

    created = tables.Column(
        verbose_name=_("Date Added"),
    )

    class Meta(PrimaryModelTable.Meta):
        model = ProjectUser
        fields = (
            "pk",
            "id",
            "user",
            "project",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "user", "project")
