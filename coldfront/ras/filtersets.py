# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.tenancy.filtersets import TenancyFilterSet
from coldfront.views.filtersets import AttributeFilterSetMixin, OrganizationalModelFilterSet, PrimaryModelFilterSet

from .choices import ResourceStatusChoices
from .models import Allocation, AllocationType, Project, Resource, ResourceType


class ResourceTypeFilterSet(OrganizationalModelFilterSet):
    class Meta:
        model = ResourceType
        fields = (
            "id",
            "name",
            "slug",
            "description",
        )


class ResourceFilterSet(AttributeFilterSetMixin, TenancyFilterSet, PrimaryModelFilterSet):
    resource_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ResourceType.objects.all(),
        distinct=False,
        label=_("Resource type (ID)"),
    )

    resource_type = django_filters.ModelMultipleChoiceFilter(
        field_name="resource_type__slug",
        queryset=ResourceType.objects.all(),
        distinct=False,
        to_field_name="slug",
        label=_("Resource type (slug)"),
    )

    status = django_filters.MultipleChoiceFilter(
        choices=ResourceStatusChoices,
        distinct=False,
        null_value=None,
    )

    class Meta:
        model = Resource
        fields = (
            "id",
            "name",
            "status",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


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


class AllocationFilterSet(AttributeFilterSetMixin, TenancyFilterSet, PrimaryModelFilterSet):
    allocation_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AllocationType.objects.all(), field_name="allocation_type_id"
    )

    class Meta:
        model = Allocation
        fields = (
            "id",
            "status",
            "allocation_type_id",
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
