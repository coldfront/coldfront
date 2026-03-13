# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelFilterSetForm, PrimaryModelFilterSetForm
from coldfront.forms.fields import TagFilterField
from coldfront.ras.choices import AllocationStatusChoices, ResourceStatusChoices
from coldfront.ras.models import Allocation, AllocationType, Project, ProjectUser, Resource, ResourceType
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
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Resource"),
            "resource_type_id",
            "status",
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
    allocation_type_id = forms.ModelMultipleChoiceField(
        queryset=AllocationType.objects.all(), required=False, label=_("Allocation Type")
    )
    project_id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label=_("Project"),
    )
    resources = forms.ModelMultipleChoiceField(
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
            "allocation_type_id",
            "project_id",
            "resources",
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


class AllocationTypeFilterSetForm(OrganizationalModelFilterSetForm):
    model = AllocationType
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            "Allocation Type",
            "q",
            "tag",
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
