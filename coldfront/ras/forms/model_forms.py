# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelForm, PrimaryModelForm
from coldfront.forms.layouts import DateTime, Slug
from coldfront.forms.mixins import AttributeProfileForm, CustomAttributesMixin
from coldfront.forms.widgets import HTMXSelect
from coldfront.ras.models import Allocation, AllocationType, Project, Resource, ResourceType
from coldfront.tenancy.forms import TenancyForm


class ResourceTypeForm(AttributeProfileForm, OrganizationalModelForm):
    class Meta:
        model = ResourceType
        fields = [
            "name",
            "slug",
            "color",
            "description",
            "schema",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Resource Type"),
            "name",
            Slug("slug"),
            "color",
            "description",
            "schema",
            "tags",
        ),
    )


class ResourceForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    resource_type = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        label=_("Resource Type"),
        required=False,
        widget=HTMXSelect(),
    )

    profile_field_name = "resource_type"

    class Meta:
        model = Resource
        fields = [
            "name",
            "resource_type",
            "status",
            "description",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Resource"),
                "name",
                "status",
                "description",
                "tags",
            ),
            Fieldset(
                "Resource Type",
                "resource_type",
                *self.attr_fields,
            ),
            Fieldset(
                _("Tenant"),
                "tenant_group",
                "tenant",
            ),
        ]


class ProjectForm(TenancyForm, OrganizationalModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "status",
            "description",
            "tags",
            "tenant",
            "tenant_group",
        ]

    fieldsets = (
        Fieldset(
            _("Project"),
            "name",
            "status",
            "description",
            "tags",
        ),
        Fieldset(
            _("Tenant"),
            "tenant_group",
            "tenant",
        ),
    )


class AllocationForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    allocation_type = forms.ModelChoiceField(
        queryset=AllocationType.objects.all(),
        label=_("Allocation Type"),
        required=False,
        widget=HTMXSelect(),
    )

    profile_field_name = "allocation_type"

    class Meta:
        model = Allocation
        fields = [
            "allocation_type",
            "project",
            "resources",
            "owner",
            "start_date",
            "end_date",
            "status",
            "description",
            "justification",
            "tags",
            "tenant",
            "tenant_group",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Allocation"),
                "project",
                "resources",
                "owner",
                DateTime("start_date"),
                DateTime("end_date"),
                "status",
                "description",
                "justification",
                "tags",
            ),
            Fieldset(
                "Allocation Type",
                "allocation_type",
                *self.attr_fields,
            ),
            Fieldset(
                _("Tenant"),
                "tenant_group",
                "tenant",
            ),
        ]


class AllocationTypeForm(AttributeProfileForm, OrganizationalModelForm):
    class Meta:
        model = AllocationType
        fields = [
            "name",
            "schema",
            "description",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Allocation Type"),
            "name",
            "description",
            "schema",
            "tags",
        ),
    )
