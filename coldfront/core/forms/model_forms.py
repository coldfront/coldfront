# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from crispy_forms.layout import Field, Fieldset
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONFormField

from coldfront.core.models import CustomFieldChoiceSet, ObjectType, Tag
from coldfront.forms.layouts import Slug
from coldfront.forms.mixins import ChangelogMessageMixin, HorizontalFormMixin
from coldfront.utils.forms.fields import ContentTypeMultipleChoiceField, SlugField


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
