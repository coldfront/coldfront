# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.ras.models import Project, ProjectUser
from coldfront.tables import OrganizationalModelTable, PrimaryModelTable, columns
from coldfront.tenancy.tables import TenancyColumnsMixin


class ProjectTable(TenancyColumnsMixin, OrganizationalModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    owner = tables.Column(
        linkify=True,
        verbose_name=_("Owner"),
    )
    user_count = columns.LinkedCountColumn(
        viewname="ras:project_users",
        view_kwargs={"pk": "pk"},
        verbose_name=_("User Count"),
    )
    allocation_count = columns.LinkedCountColumn(
        viewname="ras:project_allocations",
        view_kwargs={"pk": "pk"},
        verbose_name=_("Allocation Count"),
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
            "user_count",
            "allocation_count",
            "description",
            "tags",
            "tenant_group",
            "tenant",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "owner", "status", "description", "user_count", "allocation_count")


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
