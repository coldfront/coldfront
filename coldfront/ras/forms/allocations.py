# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from coldfront.forms import (
    PrimaryModelForm,
    PrimaryModelImportForm,
    TenancyForm,
    TenancyImportForm,
)
from coldfront.forms.fields import (
    CommentField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from coldfront.forms.layouts import DateTime
from coldfront.forms.mixins import CustomAttributesImportMixin, CustomAttributesMixin, HorizontalFormMixin
from coldfront.forms.widgets import HTMXSelectWidget
from coldfront.ras.models import Allocation, AllocationUser, Project, Resource
from coldfront.users.models import User
from coldfront.utils.forms import get_field_value


class AllocationRequestForm(CustomAttributesMixin, PrimaryModelForm):
    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput(),
    )
    resource = forms.ModelChoiceField(
        queryset=Resource.objects.all(),
        label=_("Resource"),
        required=False,
        widget=HTMXSelectWidget(),
        help_text=_("Select a resources for this allocation request"),
    )
    justification = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        help_text=_(
            "Please provide the justification for how you intend to use the resource to further the research goals of your project"
        ),
    )
    users = DynamicModelMultipleChoiceField(
        label=_("Users"),
        queryset=User.objects.all(),
        required=False,
        context={
            "checkbox": "true",
        },
        help_text=_("Please choose users"),
    )

    profile_field_name = "resource"

    class Meta:
        model = Allocation
        fields = [
            "project",
            "resource",
            "justification",
            "users",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                "Allocation Request",
                "project",
                "resource",
                *self.attr_fields,
                "justification",
                "users",
            ),
        ]

    def _get_schema(self, profile):
        if profile and profile.resource_type:
            return profile.resource_type.allocation_schema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit users queryset to those which belong to the project
        if project_id := get_field_value(self, "project"):
            project = Project.objects.filter(pk=project_id).first()
            self.fields["users"].queryset = User.objects.filter(projects__project_id=project.pk)
            self.fields["users"].widget.add_query_params({"project_id": project.pk})
        else:
            self.fields["users"].choices = ()
            self.fields["users"].widget.attrs["disabled"] = True


class AllocationReviewForm(HorizontalFormMixin, forms.ModelForm):
    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=False,
        disabled=True,
    )
    resource = forms.ModelChoiceField(
        queryset=Resource.objects.all(),
        label=_("Resource"),
        required=False,
        disabled=True,
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_("Owner"),
        required=False,
        disabled=True,
    )
    comments = CommentField()

    class Meta:
        model = Allocation
        fields = [
            "project",
            "resource",
            "owner",
            "comments",
        ]

    @property
    def fieldsets(self):
        return [
            Layout(
                "project",
                "resource",
                "owner",
                "comments",
            ),
        ]


class AllocationBaseForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    project = DynamicModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=True,
    )

    resource = forms.ModelChoiceField(
        queryset=Resource.objects.all(),
        label=_("Resource"),
        required=False,
        widget=HTMXSelectWidget(),
        help_text=_("Select a resources for this allocation request"),
    )
    owner = DynamicModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
    )
    comments = CommentField()

    profile_field_name = "resource"

    def _get_schema(self, profile):
        if profile and profile.resource_type:
            return profile.resource_type.allocation_schema


class AllocationForm(AllocationBaseForm):
    class Meta:
        model = Allocation
        fields = [
            "project",
            "resource",
            "owner",
            "start_date",
            "end_date",
            "status",
            "comments",
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
                _("Resource"),
                "resource",
                *self.attr_fields,
            ),
            Fieldset(
                _("Allocation"),
                "project",
                "owner",
                DateTime("start_date"),
                DateTime("end_date"),
                "status",
                "description",
                "justification",
            ),
            Fieldset(
                _("Comments"),
                "comments",
            ),
        ]


class AllocationActivateForm(AllocationBaseForm):
    class Meta:
        model = Allocation
        fields = [
            "project",
            "resource",
            "owner",
            "start_date",
            "end_date",
            "comments",
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
                _("Resource"),
                "resource",
                *self.attr_fields,
            ),
            Fieldset(
                _("Allocation"),
                "project",
                "owner",
                DateTime("start_date"),
                DateTime("end_date"),
                "description",
                "justification",
            ),
            Fieldset(
                _("Comments"),
                "comments",
            ),
        ]


class AllocationImportForm(CustomAttributesImportMixin, TenancyImportForm, PrimaryModelImportForm):
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

    resource = CSVModelChoiceField(
        label=_("Resource"),
        queryset=Resource.objects.all(),
        required=True,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Resource not found."),
        },
    )

    profile_field_name = "resource"

    class Meta:
        model = Allocation
        fields = [
            "project",
            "resource",
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
    allocation = forms.ModelChoiceField(
        queryset=Allocation.objects.all(),
        label=_("Allocation"),
        required=True,
        widget=HTMXSelectWidget(),
    )
    user = DynamicModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
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
                self.fields["user"].queryset = User.objects.filter(
                    Q(projects__project_id=allocation.project_id) & ~Q(allocations__allocation_id=allocation.pk)
                )
                self.fields["user"].widget.add_query_params(
                    {"available_for_allocation": f"{allocation.project_id}_{allocation.pk}"}
                )
            except ObjectDoesNotExist:
                pass


class AllocationUserImportForm(PrimaryModelImportForm):
    user = CSVModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
        to_field_name="username",
        help_text=_("User to add to allocation"),
        error_messages={
            "invalid_choice": _("User not found, is not in this project, or has already been added to the allocation."),
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

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        # Limit users to those belonging to the same project
        if self.is_bound and "allocation" in self.data:
            try:
                allocation = self.fields["allocation"].to_python(self.data["allocation"])
            except forms.ValidationError:
                allocation = None
        else:
            try:
                allocation = self.instance.allocation
            except Allocation.DoesNotExist:
                allocation = None

        if allocation:
            self.fields["user"].queryset = User.objects.filter(
                Q(projects__project_id=allocation.project_id) & ~Q(allocations__allocation_id=allocation.pk)
            )
        else:
            self.fields["user"].queryset = User.objects.none()
