# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from crispy_forms.layout import Fieldset
from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelForm, PrimaryModelForm
from coldfront.forms.layouts import DateTime, Slug
from coldfront.ras.models import Allocation, AllocationType, Project, Resource, ResourceType
from coldfront.tenancy.forms import TenancyForm
from coldfront.utils.forms.fields import JSONField
from coldfront.utils.forms.utils import get_field_value
from coldfront.utils.forms.widgets import HTMXSelect
from coldfront.utils.jsonschema import JSONSchemaProperty


class ResourceTypeForm(OrganizationalModelForm):
    class Meta:
        model = ResourceType
        fields = [
            "name",
            "slug",
            "color",
            "description",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Resource Type"),
            "name",
            Slug("slug"),
            "color",
            "description",
            "tags",
        ),
    )


class ResourceForm(TenancyForm, PrimaryModelForm):
    class Meta:
        model = Resource
        fields = [
            "name",
            "resource_type",
            "status",
            "description",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Resource"),
            "name",
            "resource_type",
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


class AllocationForm(TenancyForm, PrimaryModelForm):
    allocation_type = forms.ModelChoiceField(
        queryset=AllocationType.objects.all(),
        label=_("Allocation Type"),
        required=False,
        widget=HTMXSelect(),
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Track type-specific attribute fields
        self.attr_fields = []

        # Retrieve assigned AllocationType, if any
        if not (allocation_type_id := get_field_value(self, "allocation_type")):
            return
        if not (allocation_type := AllocationType.objects.filter(pk=allocation_type_id).first()):
            return

        # Extend form with fields for allocation attributes
        for attr, form_field in self._get_attr_form_fields(allocation_type).items():
            field_name = f"attr_{attr}"
            self.attr_fields.append(field_name)
            self.fields[field_name] = form_field
            if self.instance.attribute_data:
                self.fields[field_name].initial = self.instance.attribute_data.get(attr)

    @staticmethod
    def _get_attr_form_fields(allocation_type):
        """
        Return a dictionary mapping of attribute names to form fields, suitable for extending
        the form per the selected AllocationType.
        """
        if not allocation_type.schema:
            return {}

        properties = allocation_type.schema.get("properties", {})
        required_fields = allocation_type.schema.get("required", [])

        attr_fields = {}
        for name, options in properties.items():
            prop = JSONSchemaProperty(**options)
            attr_fields[name] = prop.to_form_field(name, required=name in required_fields)

        return dict(sorted(attr_fields.items()))

    def _post_clean(self):
        # Compile attribute data from the individual form fields
        if self.cleaned_data.get("allocation_type"):
            self.instance.attribute_data = {
                name[5:]: self.cleaned_data[name]  # Remove the attr_ prefix
                for name in self.attr_fields
                if self.cleaned_data.get(name) not in EMPTY_VALUES
            }

        return super()._post_clean()

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
                "Allocation Attributes",
                "allocation_type",
                *self.attr_fields,
            ),
            Fieldset(
                _("Tenant"),
                "tenant_group",
                "tenant",
            ),
        ]


class AllocationTypeForm(OrganizationalModelForm):
    schema = JSONField(
        label=_("Schema"),
        required=False,
        help_text=_("Enter a valid JSON schema to define supported attributes."),
    )

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
