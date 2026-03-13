# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db.models import Q

from coldfront.ras.models import Project
from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import OrganizationalModelFilterSet


class ProjectFilterSet(OrganizationalModelFilterSet, TenancyFilterSet):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "status",
            "description",
            "owner",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
