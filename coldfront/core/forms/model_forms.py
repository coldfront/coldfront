# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from crispy_forms.layout import Field, Fieldset
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONFormField

from coldfront.core.choices import CustomFieldTypeChoices
from coldfront.core.models import CustomField, CustomFieldChoiceSet, ObjectType, Tag
from coldfront.forms.layouts import Slug
from coldfront.forms.mixins import ChangelogMessageMixin, HorizontalFormMixin
from coldfront.utils.forms.fields import JSONField, SlugField
from coldfront.utils.forms.fields.content_types import ContentTypeChoiceField, ContentTypeMultipleChoiceField
from coldfront.utils.forms.utils import get_field_value


class TagForm(HorizontalFormMixin, ChangelogMessageMixin, forms.ModelForm):
    slug = SlugField()
    object_types = ContentTypeMultipleChoiceField(
        label=_("Object types"), queryset=ObjectType.objects.with_feature("tags"), required=False
    )

    class Meta:
        model = Tag
        fields = [
            "name",
            "slug",
            "color",
            "weight",
            "description",
            "object_types",
        ]

    @property
    def helper(self, *args, **kwargs):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                _("Tag"),
                Field("name"),
                Slug(),
                Field("color"),
                Field("weight"),
                Field("description"),
                Field("object_types"),
            )
        )

        return helper


class CustomFieldChoiceSetForm(HorizontalFormMixin, ChangelogMessageMixin, forms.ModelForm):
    choices = JSONFormField(
        schema=CustomFieldChoiceSet.CHOICES_SCHEMA,
        help_text=format_html(
            _("An optional label may be specified for each choice by appending it with a colon. Example:")
            + " <code>choice1:First Choice</code>"
        ),
    )

    class Meta:
        model = CustomFieldChoiceSet
        fields = [
            "name",
            "description",
            "choices",
            "order_alphabetically",
        ]

    @property
    def helper(self, *args, **kwargs):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                _("Custom Field Choice Set"),
                Field("name"),
                Field("description"),
                Field("choices"),
                Field("order_alphabetically"),
            )
        )

        return helper


class CustomFieldForm(HorizontalFormMixin, ChangelogMessageMixin, forms.ModelForm):
    object_types = ContentTypeMultipleChoiceField(
        label=_("Object types"),
        queryset=ObjectType.objects.with_feature("custom_fields"),
        help_text=_("The type(s) of object that have this custom field"),
    )
    default = JSONField(label=_("Default value"), required=False)
    related_object_type = ContentTypeChoiceField(
        label=_("Related object type"),
        queryset=ObjectType.objects.public(),
        help_text=_("Type of the related object (for object/multi-object fields only)"),
    )
    related_object_filter = JSONField(
        label=_("Related object filter"), required=False, help_text=_("Specify query parameters as a JSON object.")
    )
    choice_set = forms.ModelChoiceField(queryset=CustomFieldChoiceSet.objects.all(), required=False)

    comments = forms.CharField(required=False)

    fieldsets = (
        Fieldset(
            _("Custom Field"),
            "object_types",
            "name",
            "label",
            "group_name",
            "description",
            "type",
            "required",
            "unique",
            "default",
        ),
        Fieldset(
            _("Behavior"),
            "search_weight",
            "filter_logic",
            "ui_visible",
            "ui_editable",
            "weight",
            "is_cloneable",
        ),
    )

    class Meta:
        model = CustomField
        fields = "__all__"
        help_texts = {
            "type": _(
                "The type of data stored in this field. For object/multi-object fields, select the related object "
                "type below."
            ),
            "description": _("This will be displayed as help text for the form field. Markdown is supported."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mimic HTMXSelect()
        self.fields["type"].widget.attrs.update(
            {
                "hx-get": ".",
                "hx-include": "#form_fields",
                "hx-target": "#form_fields",
            }
        )

        # Disable changing the type of a CustomField as it almost universally causes errors if custom field data
        # is already present.
        if self.instance.pk:
            self.fields["type"].disabled = True

        field_type = get_field_value(self, "type")

        # Adjust for text fields
        if field_type in (
            CustomFieldTypeChoices.TYPE_TEXT,
            CustomFieldTypeChoices.TYPE_LONGTEXT,
        ):
            self.fieldsets = (
                self.fieldsets[0],
                Fieldset(_("Validation"), "validation_regex"),
                *self.fieldsets[1:],
            )
        else:
            del self.fields["validation_regex"]

        # Adjust for numeric fields
        if field_type in (CustomFieldTypeChoices.TYPE_INTEGER, CustomFieldTypeChoices.TYPE_DECIMAL):
            self.fieldsets = (
                self.fieldsets[0],
                Fieldset(_("Validation"), "validation_minimum", "validation_maximum"),
                *self.fieldsets[1:],
            )
        else:
            del self.fields["validation_minimum"]
            del self.fields["validation_maximum"]

        # Adjust for object & multi-object fields
        if field_type in (CustomFieldTypeChoices.TYPE_OBJECT, CustomFieldTypeChoices.TYPE_MULTIOBJECT):
            self.fieldsets = (
                self.fieldsets[0],
                Fieldset(
                    _("Related Object"),
                    "related_object_type",
                    "related_object_filter",
                ),
                *self.fieldsets[1:],
            )
        else:
            del self.fields["related_object_type"]
            del self.fields["related_object_filter"]

        # Adjust for selection & multi-select fields
        if field_type in (CustomFieldTypeChoices.TYPE_SELECT, CustomFieldTypeChoices.TYPE_MULTISELECT):
            self.fieldsets = (
                self.fieldsets[0],
                Fieldset(
                    _("Choices"),
                    "choice_set",
                ),
                *self.fieldsets[1:],
            )
        else:
            del self.fields["choice_set"]

    @property
    def helper(self, *args, **kwargs):
        helper = super().helper
        helper.layout.extend(self.fieldsets)
        return helper
