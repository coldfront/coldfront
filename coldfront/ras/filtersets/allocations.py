# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.ras.models import Allocation, AllocationType, AllocationUser, Resource
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import AttributeFilterSetMixin, OrganizationalModelFilterSet, PrimaryModelFilterSet


class AllocationFilterSet(AttributeFilterSetMixin, TenancyFilterSet, PrimaryModelFilterSet):
    allocation_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AllocationType.objects.all(), field_name="allocation_type_id"
    )
    resources = django_filters.ModelMultipleChoiceFilter(
        queryset=Resource.objects.all(),
        distinct=False,
        label=_("Resources"),
    )

    class Meta:
        model = Allocation
        fields = (
            "id",
            "status",
            "allocation_type_id",
            "resources",
            "project_id",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(owner__username__icontains=value) | Q(resources__name__icontains=value) | Q(description__icontains=value)
        )


class AllocationTypeFilterSet(OrganizationalModelFilterSet):
    class Meta:
        model = AllocationType
        fields = (
            "id",
            "name",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class AllocationUserFilterSet(PrimaryModelFilterSet):
    class Meta:
        model = AllocationUser
        fields = (
            "id",
            "allocation_id",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(user__username__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
        )
