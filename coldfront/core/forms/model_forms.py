# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from crispy_forms.layout import Field, Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.core.models import ObjectType, Tag
from coldfront.forms.layouts import Slug
from coldfront.forms.mixins import HorizontalFormMixin
from coldfront.utils.forms.fields import ContentTypeMultipleChoiceField, SlugField


class TagForm(HorizontalFormMixin, forms.ModelForm):
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
