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
    Project,
    ProjectUser,
    Resource,
    ResourceType,
)
from coldfront.tenancy.forms import TenancyFilterSetForm
from coldfront.users.models import User


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
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_("Owner"),
        required=False,
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Project"),
            "owner",
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
    status = forms.MultipleChoiceField(
        label=_("Status"),
        choices=AllocationStatusChoices,
        required=False,
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_("Owner"),
        required=False,
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Allocation"),
            "project_id",
            "status",
            "owner",
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
