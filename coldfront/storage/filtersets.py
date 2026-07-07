# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.storage.models import StorageCluster, StorageQuota, StorageResource, StorageSnapshotPolicy
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import PrimaryModelFilterSet


class StorageResourceFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
    clusters = django_filters.ModelMultipleChoiceFilter(
        queryset=StorageCluster.objects.all(),
        distinct=False,
        label=_("Clusters"),
    )

    class Meta:
        model = StorageResource
        fields = (
            "id",
            "name",
            "description",
            "clusters",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class StorageClusterFilterSet(PrimaryModelFilterSet):
    class Meta:
        model = StorageCluster
        fields = (
            "id",
            "name",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class StorageQuotaFilterSet(PrimaryModelFilterSet):
    storage_id = django_filters.ModelMultipleChoiceFilter(
        queryset=StorageResource.objects.all(),
        distinct=False,
        label=_("Storage Resource (ID)"),
    )
    storage = django_filters.ModelMultipleChoiceFilter(
        field_name="storage__name",
        queryset=StorageResource.objects.all(),
        distinct=False,
        to_field_name="name",
        label=_("Storage Resource (name)"),
    )

    class Meta:
        model = StorageQuota
        fields = (
            "id",
            "storage",
            "path",
            "owning_user",
            "owning_group",
            "state",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(path__icontains=value) | Q(owning_user__icontains=value) | Q(owning_group__icontains=value)
        )


class StorageSnapshotPolicyFilterSet(PrimaryModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=StorageCluster.objects.all(),
        distinct=False,
        label=_("Cluster (ID)"),
    )
    cluster = django_filters.ModelMultipleChoiceFilter(
        field_name="cluster__name",
        queryset=StorageCluster.objects.all(),
        distinct=False,
        to_field_name="name",
        label=_("Cluster (name)"),
    )

    class Meta:
        model = StorageSnapshotPolicy
        fields = (
            "id",
            "cluster",
            "name",
            "interval",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))
