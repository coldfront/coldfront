# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.core.models import ObjectType
from coldfront.ras.models import Allocation, Project
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import AttributeFilterSetMixin, PrimaryModelFilterSet


class AllocationFilterSet(AttributeFilterSetMixin, TenancyFilterSet, PrimaryModelFilterSet):
    project_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Project.objects.all(),
        distinct=False,
        label=_("Projects"),
    )
    resource_object_type_id = django_filters.ModelChoiceFilter(
        field_name="resource_object_type",
        queryset=ObjectType.objects.with_feature("allocatable_resource"),
        label=_("Resource Object"),
    )
    start_date = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="gte",
        label=_("Start date (on or after)"),
    )
    end_date = django_filters.DateFilter(
        field_name="end_date",
        lookup_expr="lte",
        label=_("End date (on or before)"),
    )

    class Meta:
        model = Allocation
        fields = (
            "id",
            "status",
            "project_id",
            "owner",
            "resource_object_type_id",
            "start_date",
            "end_date",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(owner__username__icontains=value)
            | Q(project__name__icontains=value)
            | Q(justification__icontains=value)
            | Q(description__icontains=value)
            | Q(comments__icontains=value)
        )
