# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.ras.models import Allocation, AllocationUser, Resource
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import AttributeFilterSetMixin, PrimaryModelFilterSet


class AllocationFilterSet(AttributeFilterSetMixin, TenancyFilterSet, PrimaryModelFilterSet):
    resource_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Resource.objects.all(),
        distinct=False,
        label=_("Resources"),
    )

    class Meta:
        model = Allocation
        fields = (
            "id",
            "status",
            "resource_id",
            "project_id",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(owner__username__icontains=value) | Q(resources__name__icontains=value) | Q(description__icontains=value)
        )


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
