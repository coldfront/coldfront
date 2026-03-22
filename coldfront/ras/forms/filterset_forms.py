# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelFilterSetForm, PrimaryModelFilterSetForm
from coldfront.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from coldfront.ras.choices import AllocationStatusChoices, ResourceStatusChoices
from coldfront.ras.models import (
    Allocation,
    AllocationUser,
    Project,
    ProjectUser,
    Resource,
    ResourceType,
)
from coldfront.tenancy.forms import TenancyFilterSetForm


class ResourceTypeFilterSetForm(OrganizationalModelFilterSetForm):
    model = ResourceType
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            "Resource Type",
            "tag",
        ),
    )


class ResourceFilterSetForm(TenancyFilterSetForm, PrimaryModelFilterSetForm):
    model = Resource
    resource_type_id = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        required=False,
        label=_("Resource Type"),
    )
    status = forms.MultipleChoiceField(
        label=_("Status"),
        choices=ResourceStatusChoices,
        required=False,
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Resource.objects.all(),
        required=False,
        label=_("Parent"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Resource"),
            "resource_type_id",
            "status",
            "parent_id",
            "tag",
        ),
        Fieldset(
            _("Tenant"),
            "tenant_group_id",
            "tenant_id",
        ),
    )


class ProjectFilterSetForm(TenancyFilterSetForm, OrganizationalModelFilterSetForm):
    model = Project
    status = forms.MultipleChoiceField(
        label=_("Status"),
        choices=ResourceStatusChoices,
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        required=False,
    )
    username = forms.CharField(
        label="PI Username",
        max_length=100,
        required=False,
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Project"),
            "status",
            "last_name",
            "username",
            "tag",
        ),
        Fieldset(
            _("Tenant"),
            "tenant_group_id",
            "tenant_id",
        ),
    )


class AllocationFilterSetForm(TenancyFilterSetForm, PrimaryModelFilterSetForm):
    model = Allocation
    project_id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label=_("Project"),
    )
    resource_id = forms.ModelMultipleChoiceField(
        queryset=Resource.objects.all(),
        required=False,
        label=_("Resources"),
    )
    status = forms.MultipleChoiceField(
        label=_("Status"),
        choices=AllocationStatusChoices,
        required=False,
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        required=False,
    )
    username = forms.CharField(
        label="PI Username",
        max_length=100,
        required=False,
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Allocation"),
            "project_id",
            "resource_id",
            "status",
            "last_name",
            "username",
            "tag",
        ),
        Fieldset(
            _("Tenant"),
            "tenant_group_id",
            "tenant_id",
        ),
    )


class ProjectUserFilterSetForm(PrimaryModelFilterSetForm):
    model = ProjectUser
    project_id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label=_("Project"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("User"),
            "q",
            "project_id",
            "tag",
        ),
    )


class AllocationUserFilterSetForm(PrimaryModelFilterSetForm):
    model = AllocationUser
    allocation_id = forms.ModelChoiceField(
        queryset=Allocation.objects.all(),
        required=False,
        label=_("Allocation"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("User"),
            "q",
            "allocation_id",
            "tag",
        ),
    )
