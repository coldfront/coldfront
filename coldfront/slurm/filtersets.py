# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.slurm.models import SlurmCluster, SlurmPartition
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import PrimaryModelFilterSet


class SlurmClusterFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
    class Meta:
        model = SlurmCluster
        fields = (
            "id",
            "name",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class SlurmPartitionFilterSet(PrimaryModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SlurmCluster.objects.all(),
        distinct=False,
        label=_("Cluster (ID)"),
    )
    cluster = django_filters.ModelMultipleChoiceFilter(
        field_name="cluster__name",
        queryset=SlurmCluster.objects.all(),
        distinct=False,
        to_field_name="name",
        label=_("Cluster (name)"),
    )

    class Meta:
        model = SlurmPartition
        fields = (
            "id",
            "cluster",
            "name",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
