# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django_tables2.utils import Accessor

from coldfront.ras.models import Allocation, AllocationUser
from coldfront.tables import PrimaryModelTable, columns
from coldfront.tenancy.tables import TenancyColumnsMixin

from .template_code import ALLOCATION_STATUS_ACTIONS


class AllocationTable(TenancyColumnsMixin, PrimaryModelTable):
    actions = columns.ActionsColumn(
        extra_buttons=ALLOCATION_STATUS_ACTIONS,
    )

    slug = tables.Column(
        verbose_name=_("Allocation"),
        linkify=True,
    )

    project = tables.Column(
        verbose_name=_("Project"),
        linkify=True,
    )
    owner = tables.Column(
        verbose_name=_("Owner"),
    )

    resource = tables.Column(
        verbose_name=_("Resource"),
        linkify=True,
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
        url_name="ras:allocation_list",
    )

    class Meta(PrimaryModelTable.Meta):
        model = Allocation
        fields = (
            "pk",
            "id",
            "slug",
            "project",
            "owner",
            "resource",
            "status",
            "description",
            "justification",
            "tags",
            "tenant_group",
            "tenant",
            "start_date",
            "end_date",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "slug", "resource", "owner", "project", "status", "start_date", "end_date")


class AllocationUserTable(PrimaryModelTable):
    user = tables.Column(
        linkify=("ras:allocationuser", {"pk": tables.A("id")}),
        verbose_name=_("User"),
    )

    allocation = tables.Column(
        verbose_name=_("Allocation"),
        linkify=True,
    )

    project = tables.Column(
        accessor=Accessor("allocation__project"),
        verbose_name=_("Project"),
        linkify=True,
    )

    owner = tables.Column(
        accessor=Accessor("allocation__owner"),
        verbose_name=_("Owner"),
    )

    created = tables.Column(
        verbose_name=_("Date Added"),
    )

    class Meta(PrimaryModelTable.Meta):
        model = AllocationUser
        fields = (
            "pk",
            "id",
            "user",
            "allocation",
            "project",
            "owner",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "user", "allocation", "project", "owner")
