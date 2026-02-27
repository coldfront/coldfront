# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import time

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.db.models import Q
from django.utils.translation import gettext as _

from coldfront.core.choices import CustomFieldUIEditableChoices
from coldfront.core.models import CustomField, ObjectType, Tag

__all__ = ("TagsMixin",)


class HorizontalFormMixin:
    """
    Mixin for horizontal form layouts with crispy
    """

    @property
    def helper(self):
        """
        crispy forms helper which defines the form rendering behavior.
        """
        helper = FormHelper()
        helper.form_tag = False
        helper.form_class = "form-horizontal"
        helper.label_class = "col-lg-3 text-end"
        helper.field_class = "col-lg-6"
        helper.layout = Layout(*self.fieldsets)
        return helper


class TagsMixin(forms.Form):
    """
    Mixin for forms that support tagging.

    Provides a field for selecting tags,
    with options limited to those applicable to the form's model.
    """

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label=_("Tags"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit tags to those applicable to the object type
        object_type = ObjectType.objects.get_for_model(self._meta.model)
        self.fields["tags"].queryset = self.fields["tags"].queryset.filter(
            Q(object_types__id=object_type.pk) | Q(object_types__isnull=True)
        )


class ChangelogMessageMixin(forms.Form):
    """
    Adds an optional field for recording a message on the resulting changelog record(s).
    """

    changelog_message = forms.CharField(
        required=False,
        max_length=200,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Declare changelog_message a meta field
        if hasattr(self, "meta_fields"):
            self.meta_fields.append("changelog_message")
        else:
            self.meta_fields = ["changelog_message"]


class CheckLastUpdatedMixin(forms.Form):
    """
    Checks whether the object being saved has been updated since the form was initialized. If so, validation fails.
    This prevents a user from inadvertently overwriting any changes made to the object between when the form was
    initialized and when it was submitted.

    This validation does not apply to newly created objects, or if the `_init_time` field is not present in the form
    data.
    """

    _init_time = forms.DecimalField(initial=time.time, required=False, widget=forms.HiddenInput())

    def clean(self):
        super().clean()

        # Skip for absent or newly created instances
        if not self.instance or not self.instance.pk:
            return

        # Skip if a form init time has not been specified
        if not (form_init_time := self.cleaned_data.get("_init_time")):
            return

        # Skip if the object does not have a last_updated value
        if not (last_updated := getattr(self.instance, "last_updated", None)):
            return

        # Check that the submitted initialization time is not earlier than the object's modification time
        if form_init_time < last_updated.timestamp():
            raise forms.ValidationError(
                _(
                    "This object has been modified since the form was rendered. Please consult the object's change "
                    "log for details."
                )
            )


class CustomFieldsMixin:
    """
    Extend a Form to include custom field support.

    Attributes:
        model: The model class
    """

    model = None

    def __init__(self, *args, **kwargs):
        self.custom_fields = {}
        self.custom_field_groups = {}

        super().__init__(*args, **kwargs)

        self._append_customfield_fields()

    def _get_content_type(self):
        """
        Return the ObjectType of the form's model.
        """
        if not getattr(self, "model", None):
            raise NotImplementedError(
                _("{class_name} must specify a model class.").format(class_name=self.__class__.__name__)
            )
        return ObjectType.objects.get_for_model(self.model)

    def _get_custom_fields(self, content_type):
        # Return only custom fields that are not hidden from the UI
        return [
            cf
            for cf in CustomField.objects.get_for_model(content_type.model_class())
            if cf.ui_editable != CustomFieldUIEditableChoices.HIDDEN
        ]

    def _get_form_field(self, customfield):
        return customfield.to_form_field()

    def _append_customfield_fields(self):
        """
        Append form fields for all CustomFields assigned to this object type.
        """
        for customfield in self._get_custom_fields(self._get_content_type()):
            field_name = f"cf_{customfield.name}"
            self.fields[field_name] = self._get_form_field(customfield)

            # Annotate the field in the list of CustomField form fields
            self.custom_fields[field_name] = customfield
            if customfield.group_name not in self.custom_field_groups:
                self.custom_field_groups[customfield.group_name] = []
            self.custom_field_groups[customfield.group_name].append(field_name)
