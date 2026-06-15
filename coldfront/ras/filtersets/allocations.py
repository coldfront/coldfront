# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.ras.models import Allocation, Project
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import AttributeFilterSetMixin, PrimaryModelFilterSet


class AllocationFilterSet(AttributeFilterSetMixin, TenancyFilterSet, PrimaryModelFilterSet):
    project_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Project.objects.all(),
        distinct=False,
        label=_("Projects"),
    )

    class Meta:
        model = Allocation
        fields = (
            "id",
            "status",
            "project_id",
            "owner",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(owner__username__icontains=value) | Q(project__name__icontains=value))
