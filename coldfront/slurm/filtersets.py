# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.slurm.models import (
    SlurmAccount,
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmQOS,
    SlurmUser,
)
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import PrimaryModelFilterSet


class SlurmQOSFilterSet(PrimaryModelFilterSet):
    class Meta:
        model = SlurmQOS
        fields = (
            "id",
            "name",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


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
            "nodes",
            "priority",
            "is_default",
            "state",
            "preempt_mode",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class SlurmAccountFilterSet(PrimaryModelFilterSet):
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
        model = SlurmAccount
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


class SlurmAssociationFilterSet(PrimaryModelFilterSet):
    slurm_account_id = django_filters.ModelChoiceFilter(
        queryset=SlurmAccount.objects.all(),
        label=_("Slurm Account"),
    )

    class Meta:
        model = SlurmAssociation
        fields = (
            "id",
            "slurm_account",
            "fairshare",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(allocation__slug__icontains=value))


class SlurmUserFilterSet(PrimaryModelFilterSet):
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
        model = SlurmUser
        fields = (
            "id",
            "cluster",
            "admin_level",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(user__username__icontains=value) | Q(user__email__icontains=value))
