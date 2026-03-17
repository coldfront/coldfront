# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import (
    OrganizationalModelForm,
    PrimaryModelForm,
    PrimaryModelImportForm,
    TenancyForm,
    TenancyImportForm,
)
from coldfront.forms.fields import CSVModelChoiceField
from coldfront.forms.layouts import Slug
from coldfront.forms.mixins import AttributeProfileForm, CustomAttributesImportMixin, CustomAttributesMixin
from coldfront.forms.widgets import HTMXSelect
from coldfront.ras.models import Resource, ResourceType


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
        ),
    )


class ResourceForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    resource_type = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        label=_("Resource Type"),
        required=True,
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
            "tenant",
            "tenant_group",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Resource"),
                "name",
                "status",
                "description",
            ),
            Fieldset(
                "Resource Type",
                "resource_type",
                *self.attr_fields,
            ),
        ]


class ResourceImportForm(CustomAttributesImportMixin, TenancyImportForm, PrimaryModelImportForm):
    resource_type = CSVModelChoiceField(
        label=_("Resource Type"),
        queryset=ResourceType.objects.all(),
        to_field_name="name",
        help_text=_("Resource Type"),
    )

    attribute_data = forms.JSONField(
        label=_("Attributes"),
        required=False,
        help_text=_("Attribute values for the assigned resource type, passed as a dictionary"),
    )

    profile_field_name = "resource_type"

    class Meta:
        model = Resource
        fields = [
            "name",
            "resource_type",
            "status",
            "description",
            "attribute_data",
            "tags",
            "tenant",
            "tenant_group",
        ]


class ResourceTypeImportForm(PrimaryModelImportForm):
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
