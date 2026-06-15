# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
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
)
from coldfront.forms.layouts import DateTime
from coldfront.forms.mixins import CustomAttributesImportMixin, CustomAttributesMixin, HorizontalFormMixin
from coldfront.forms.widgets import HTMXSelectWidget
from coldfront.ras.models import Allocation, Project
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


def _get_schema_from_resource_object_value(value):
    """Given a ``resource_object`` form value (``ct_id:obj_id``), return the allocation schema."""
    try:
        ct_id, object_id = value.split(":")
        ct = ContentType.objects.get(pk=ct_id)
        obj = ct.get_object_for_this_type(pk=object_id)
        return obj.get_allocation_attribute_schema()
    except (ValueError, ContentType.DoesNotExist, ObjectDoesNotExist):
        return None


class AllocationResourceObjectMixin(forms.Form):
    """
    Mixin that provides the ``resource_object`` ChoiceField, validation, and saving
    logic shared by AllocationRequestForm and AllocationBaseForm.
    """

    resource_object = forms.ChoiceField(
        choices=[],
        label=_("Resource"),
        widget=HTMXSelectWidget(),
        help_text=_("Select a resources for this allocation request"),
    )

    profile_field_name = "resource_object"

    def _get_schema(self):
        if ro := get_field_value(self, "resource_object"):
            return _get_schema_from_resource_object_value(ro)
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["resource_object"].choices = _get_resource_object_choices()

    def clean_resource_object(self):
        data = self.cleaned_data["resource_object"]
        try:
            ct_id, object_id = data.split(":")
            ct = ContentType.objects.get(pk=ct_id)
            ct.get_object_for_this_type(pk=object_id)
        except (ValueError, ContentType.DoesNotExist, ObjectDoesNotExist):
            raise forms.ValidationError(_("Selected resource object does not exist."))
        return {"content_type": ct, "object_id": object_id}

    def save_resource_object(self, instance):
        resource_data = self.cleaned_data["resource_object"]
        instance.resource_object_type = resource_data["content_type"]
        instance.resource_object_id = resource_data["object_id"]


class AllocationRequestForm(AllocationResourceObjectMixin, CustomAttributesMixin, PrimaryModelForm):
    project = forms.ModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=False,
        disabled=True,
        widget=forms.HiddenInput(),
    )

    justification = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        help_text=_(
            "Please provide the justification for how you intend to use the resource"
            " to further the research goals of your project"
        ),
    )

    class Meta:
        model = Allocation
        # resource_object is a GenericForeignKey; handled by AllocationResourceObjectMixin
        fields = [
            "project",
            "justification",
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
            ),
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        self.save_resource_object(instance)
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


class AllocationBaseForm(AllocationResourceObjectMixin, TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    project = DynamicModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=True,
    )

    owner = DynamicModelChoiceField(
        label=_("Owner"),
        queryset=User.objects.all(),
        required=True,
    )
    comments = CommentField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial value for resource_object when editing an existing instance
        if self.instance and self.instance.pk and self.instance.resource_object:
            ct = ContentType.objects.get_for_model(self.instance.resource_object)
            value = f"{ct.id}:{self.instance.resource_object_id}"
            self.fields["resource_object"].initial = value

    def save(self, commit=True):
        instance = super().save(commit=False)
        self.save_resource_object(instance)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class AllocationForm(AllocationBaseForm):
    class Meta:
        model = Allocation
        # resource_object is a GenericForeignKey; handled by AllocationResourceObjectMixin
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
        # resource_object is a GenericForeignKey; handled by AllocationResourceObjectMixin
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
