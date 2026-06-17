# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.slurm.models import SlurmCluster, SlurmPartition
from coldfront.tables import PrimaryModelTable, columns
from coldfront.tenancy.tables.columns import TenancyColumnsMixin


class SlurmClusterTable(TenancyColumnsMixin, PrimaryModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    partition_count = columns.LinkedCountColumn(
        viewname="slurm:slurmpartition_list",
        url_params={"cluster_id": "pk"},
        verbose_name=_("Partition Count"),
    )
    tags = columns.TagColumn(
        url_name="slurm:slurmcluster_list",
    )

    class Meta(PrimaryModelTable.Meta):
        model = SlurmCluster
        fields = (
            "pk",
            "id",
            "name",
            "description",
            "tenant",
            "is_allocatable",
            "partition_count",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "description", "partition_count", "is_allocatable")


class SlurmPartitionTable(PrimaryModelTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    cluster = columns.ColoredLabelColumn(
        verbose_name=_("Cluster"),
    )
    tags = columns.TagColumn(
        url_name="slurm:slurmpartition_list",
    )

    class Meta(PrimaryModelTable.Meta):
        model = SlurmPartition
        fields = (
            "pk",
            "id",
            "cluster",
            "name",
            "description",
            "is_allocatable",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "cluster", "name", "description", "is_allocatable")
