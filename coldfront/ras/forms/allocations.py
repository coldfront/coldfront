# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelForm, PrimaryModelForm, PrimaryModelImportForm
from coldfront.forms.fields import (
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from coldfront.forms.layouts import DateTime
from coldfront.forms.mixins import AttributeProfileForm, CustomAttributesImportMixin, CustomAttributesMixin
from coldfront.forms.widgets import HTMXSelect
from coldfront.ras.models import Allocation, AllocationType, Project, Resource
from coldfront.tenancy.forms import TenancyForm, TenancyImportForm
from coldfront.users.models import User


class AllocationForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    allocation_type = forms.ModelChoiceField(
        queryset=AllocationType.objects.all(),
        label=_("Allocation Type"),
        required=True,
        widget=HTMXSelect(),
    )
    project = DynamicModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=True,
    )
    resources = DynamicModelMultipleChoiceField(
        label=_("Resource"),
        queryset=Resource.objects.all(),
        required=True,
        selector=True,
    )
    owner = DynamicModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
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


class AllocationTypeImportForm(PrimaryModelImportForm):
    class Meta:
        model = AllocationType
        fields = [
            "name",
            "schema",
            "description",
            "tags",
        ]


class AllocationImportForm(CustomAttributesImportMixin, TenancyImportForm, PrimaryModelImportForm):
    allocation_type = CSVModelChoiceField(
        label=_("Allocation Type"),
        queryset=AllocationType.objects.all(),
        to_field_name="name",
        help_text=_("Allocation Type"),
    )

    attribute_data = forms.JSONField(
        label=_("Attributes"),
        required=False,
        help_text=_("Attribute values for the assigned allocation type, passed as a dictionary"),
    )

    owner = CSVModelChoiceField(
        label=_("Owner"),
        queryset=User.objects.all(),
        required=True,
        to_field_name="username",
        help_text=_("The owner of the allocation"),
        error_messages={
            "invalid_choice": _("User not found."),
        },
    )

    project = CSVModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=True,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Project not found."),
        },
    )

    resources = CSVModelMultipleChoiceField(
        label=_("Resources"),
        queryset=Resource.objects.all(),
        required=True,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Resource not found."),
        },
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
