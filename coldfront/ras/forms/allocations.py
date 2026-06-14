# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from coldfront.core.models import ObjectType
from coldfront.forms import (
    PrimaryModelForm,
    PrimaryModelImportForm,
    TenancyForm,
    TenancyImportForm,
)
from coldfront.forms.fields import (
    CommentField,
    CSVContentTypeObjectField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from coldfront.forms.layouts import DateTime
from coldfront.forms.mixins import CustomAttributesImportMixin, CustomAttributesMixin, HorizontalFormMixin
from coldfront.forms.widgets import HTMXSelectWidget
from coldfront.ras.models import Allocation, AllocationUser, Project
from coldfront.users.models import User
from coldfront.utils.forms import add_blank_choice, get_field_value


def _get_resource_object_choices():
    """
    Build a list of optgroup choices for all objects with the "allocatable_resource" feature.
    Returns a list of (optgroup_label, [(value, label), ...]) tuples.
    """
    choices = []
    for ot in ObjectType.objects.with_feature("allocatable_resource").order_by("app_label", "model"):
        model_class = ot.model_class()
        if model_class is None:
            continue
        ct = ContentType.objects.get_for_model(model_class)
        model_choices = []
        for obj in model_class.objects.all():
            if not obj.is_allocatable:
                continue
            value = f"{ct.id}:{obj.id}"
            label = str(obj)
            model_choices.append((value, label))
        optgroup_label = model_class._meta.verbose_name_plural.title()
        choices.append((optgroup_label, model_choices))
    return add_blank_choice(choices)


class AllocationRequestForm(CustomAttributesMixin, PrimaryModelForm):
    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput(),
    )

    resource_object = forms.ChoiceField(
        choices=[],
        label=_("Resource"),
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

    profile_field_name = "resource_object"

    class Meta:
        model = Allocation
        # resource_object is a GenericForeignKey and cannot be auto-generated as a form field;
        # it is declared explicitly above and handled in clean/save.
        fields = [
            "project",
            "justification",
            "users",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                "Allocation Request",
                "project",
                "resource_object",
                *self.attr_fields,
                "justification",
                "users",
            ),
        ]

    def _get_schema(self):
        if ro := get_field_value(self, "resource_object"):
            try:
                ct_id, object_id = ro.split(":")
                ct = ContentType.objects.get(pk=ct_id)
                obj = ct.get_object_for_this_type(pk=object_id)
                return obj.get_allocation_attribute_schema()
            except (ValueError, ContentType.DoesNotExist, ObjectDoesNotExist):
                pass

        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate resource_object choices with all allocatable objects
        self.fields["resource_object"].choices = _get_resource_object_choices()

        # Limit users queryset to those which belong to the project
        if project_id := get_field_value(self, "project"):
            project = Project.objects.filter(pk=project_id).first()
            self.fields["users"].queryset = User.objects.filter(projects__project_id=project.pk)
            self.fields["users"].widget.add_query_params({"project_id": project.pk})
        else:
            self.fields["users"].choices = ()
            self.fields["users"].widget.attrs["disabled"] = True

    def clean_resource_object(self):
        data = self.cleaned_data["resource_object"]
        try:
            ct_id, object_id = data.split(":")
            ct = ContentType.objects.get(pk=ct_id)
            ct.get_object_for_this_type(pk=object_id)
        except (ValueError, ContentType.DoesNotExist, ObjectDoesNotExist):
            raise forms.ValidationError(_("Selected resource object does not exist."))
        return {"content_type": ct, "object_id": object_id}

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Pull the validated resource_object data and map it to the real fields
        resource_data = self.cleaned_data["resource_object"]
        instance.resource_object_type = resource_data["content_type"]
        instance.resource_object_id = resource_data["object_id"]

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class AllocationReviewForm(HorizontalFormMixin, forms.ModelForm):
    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
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
            "owner",
            "comments",
        ]

    @property
    def fieldsets(self):
        return [
            Layout(
                "project",
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

    resource_object = forms.ChoiceField(
        choices=[],
        label=_("Resource"),
        widget=HTMXSelectWidget(),
        help_text=_("Select a resources for this allocation request"),
    )

    owner = DynamicModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
    )
    comments = CommentField()

    profile_field_name = "resource_object"

    def _get_schema(self):
        if ro := get_field_value(self, "resource_object"):
            try:
                ct_id, object_id = ro.split(":")
                ct = ContentType.objects.get(pk=ct_id)
                obj = ct.get_object_for_this_type(pk=object_id)
                return obj.get_allocation_attribute_schema()
            except (ValueError, ContentType.DoesNotExist, ObjectDoesNotExist):
                pass

        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate resource_object choices with all allocatable objects
        self.fields["resource_object"].choices = _get_resource_object_choices()

        # Set initial value for resource_object when editing an existing instance
        if self.instance and self.instance.pk and self.instance.resource_object:
            ct = ContentType.objects.get_for_model(self.instance.resource_object)
            value = f"{ct.id}:{self.instance.resource_object_id}"
            self.fields["resource_object"].initial = value

    def clean_resource_object(self):
        data = self.cleaned_data["resource_object"]
        try:
            ct_id, object_id = data.split(":")
            ct = ContentType.objects.get(pk=ct_id)
            ct.get_object_for_this_type(pk=object_id)
        except (ValueError, ContentType.DoesNotExist, ObjectDoesNotExist):
            raise forms.ValidationError(_("Selected resource object does not exist."))
        return {"content_type": ct, "object_id": object_id}

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Pull the validated resource_object data and map it to the real fields
        resource_data = self.cleaned_data["resource_object"]
        instance.resource_object_type = resource_data["content_type"]
        instance.resource_object_id = resource_data["object_id"]

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class AllocationForm(AllocationBaseForm):
    class Meta:
        model = Allocation
        # resource_object is a GenericForeignKey; handled explicitly in AllocationBaseForm
        fields = [
            "project",
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
                "resource_object",
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
        # resource_object is a GenericForeignKey; handled explicitly in AllocationBaseForm
        fields = [
            "project",
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
                "resource_object",
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

    resource_object = CSVContentTypeObjectField(
        label=_("Resource"),
        required=True,
        to_field_name="name",
        help_text=_("Resource in the format <app_label>.<model>:<name> (e.g. ras.resource:My Cluster)"),
        error_messages={
            "invalid_choice": _("Resource not found."),
        },
    )

    profile_field_name = "resource_object"

    class Meta:
        model = Allocation
        # resource_object is handled explicitly by CSVContentTypeObjectField
        fields = [
            "project",
            "owner",
            "start_date",
            "end_date",
            "status",
            "description",
            "justification",
            "tags",
            "tenant",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Map the resolved resource_object to the GenericForeignKey fields
        resource_obj = self.cleaned_data.get("resource_object")
        if resource_obj:
            instance.resource_object_type = ContentType.objects.get_for_model(resource_obj)
            instance.resource_object_id = resource_obj.pk

        if commit:
            instance.save()
            self.save_m2m()
        return instance


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
