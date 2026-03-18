# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from coldfront.forms import (
    OrganizationalModelForm,
    PrimaryModelForm,
    PrimaryModelImportForm,
    TenancyForm,
    TenancyImportForm,
)
from coldfront.forms.fields import (
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from coldfront.forms.layouts import DateTime
from coldfront.forms.mixins import AttributeProfileForm, CustomAttributesImportMixin, CustomAttributesMixin
from coldfront.forms.widgets import HTMXSelect
from coldfront.ras.models import Allocation, AllocationType, AllocationUser, Project, ProjectUser, Resource
from coldfront.users.models import User
from coldfront.utils.forms import get_field_value


class AllocationForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    allocation_type = forms.ModelChoiceField(
        queryset=AllocationType.objects.all(),
        label=_("Allocation Type"),
        required=False,
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
            ),
            Fieldset(
                "Allocation Type",
                "allocation_type",
                *self.attr_fields,
            ),
        ]


class AllocationTypeForm(AttributeProfileForm, OrganizationalModelForm):
    class Meta:
        model = AllocationType
        fields = [
            "name",
            "schema",
            "description",
            "is_default",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Allocation Type"),
            "name",
            "description",
            "schema",
            "is_default",
        ),
    )


class AllocationTypeImportForm(PrimaryModelImportForm):
    class Meta:
        model = AllocationType
        fields = [
            "name",
            "schema",
            "description",
            "is_default",
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
        ]


class AllocationUserForm(PrimaryModelForm):
    user = DynamicModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
        selector=True,
        context={
            "label": "username",
            "title": "Username,First Name,Last Name,Email",
            "extra-columns": "first_name,last_name,email",
        },
    )

    class Meta:
        model = AllocationUser
        fields = [
            "allocation",
            "user",
        ]

    fieldsets = (
        Fieldset(
            _("Allocation User"),
            "allocation",
            "user",
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if allocation_id := get_field_value(self, "allocation"):
            try:
                allocation = Allocation.objects.get(pk=allocation_id)
                self.fields["user"].widget.add_query_params({"project_id": allocation.project_id})
                self.fields["allocation"].widget.attrs["data-readonly"] = "readonly"
            except ObjectDoesNotExist:
                pass

    def clean(self):
        super().clean()
        allocation = self.cleaned_data["allocation"]
        user = self.cleaned_data["user"]
        try:
            ProjectUser.objects.get(project_id=allocation.project_id, user_id=user.id)
        except ObjectDoesNotExist:
            # TODO: should we enforce this?
            raise forms.ValidationError(_("You can only add users that are on the same project as the allocation."))


class AllocationUserImportForm(PrimaryModelImportForm):
    user = CSVModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
        to_field_name="username",
        help_text=_("User to add to allocation"),
        error_messages={
            "invalid_choice": _("User not found."),
        },
    )

    allocation = CSVModelChoiceField(
        label=_("Allocation"),
        queryset=Allocation.objects.all(),
        required=True,
        to_field_name="slug",
        error_messages={
            "invalid_choice": _("Allocation not found."),
        },
    )

    class Meta:
        model = AllocationUser
        fields = [
            "user",
            "allocation",
        ]
