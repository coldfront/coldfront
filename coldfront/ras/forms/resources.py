# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import (
    NestedGroupModelForm,
    NestedGroupModelImportForm,
    OrganizationalModelForm,
    PrimaryModelImportForm,
    TenancyForm,
    TenancyImportForm,
)
from coldfront.forms.fields import CSVModelChoiceField, DynamicModelChoiceField, SlugField
from coldfront.forms.layouts import Slug
from coldfront.forms.mixins import AttributeProfileForm, CustomAttributesImportMixin, CustomAttributesMixin
from coldfront.forms.widgets import HTMXSelect
from coldfront.ras.models import Resource, ResourceType


class ResourceTypeForm(AttributeProfileForm, OrganizationalModelForm):
    slug = SlugField()

    class Meta:
        model = ResourceType
        fields = [
            "name",
            "slug",
            "color",
            "description",
            "schema",
            "is_default",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Resource Type"),
            "name",
            Slug(),
            "color",
            "description",
            "schema",
            "is_default",
        ),
    )


class ResourceForm(TenancyForm, CustomAttributesMixin, NestedGroupModelForm):
    resource_type = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        label=_("Resource Type"),
        required=False,
        widget=HTMXSelect(),
    )

    parent = DynamicModelChoiceField(
        label=_("Parent"),
        queryset=Resource.objects.all(),
        required=False,
    )

    profile_field_name = "resource_type"

    class Meta:
        model = Resource
        fields = [
            "name",
            "slug",
            "parent",
            "resource_type",
            "status",
            "description",
            "tags",
            "tenant_group",
            "tenant",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Resource"),
                "name",
                Slug(),
                "parent",
                "status",
                "description",
            ),
            Fieldset(
                "Resource Type",
                "resource_type",
                *self.attr_fields,
            ),
        ]


class ResourceImportForm(CustomAttributesImportMixin, TenancyImportForm, NestedGroupModelImportForm):
    parent = CSVModelChoiceField(
        label=_("Parent"),
        queryset=Resource.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Parent resource"),
    )

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
            "slug",
            "resource_type",
            "parent",
            "status",
            "description",
            "attribute_data",
            "tags",
            "tenant",
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
            "is_default",
            "tags",
        ]
