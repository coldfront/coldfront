# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.core.choices import ObjectChangeActionChoices
from coldfront.core.models import CustomFieldChoiceSet, ObjectChange, ObjectType, Tag
from coldfront.forms import PrimaryModelFilterSetForm
from coldfront.forms.layouts import DateTime
from coldfront.users.models import User
from coldfront.utils.forms import add_blank_choice
from coldfront.utils.forms.fields import (
    ContentTypeChoiceField,
    ContentTypeMultipleChoiceField,
)

__all__ = ("TagFilterForm",)


class TagFilterForm(PrimaryModelFilterSetForm):
    model = Tag
    content_type_id = ContentTypeMultipleChoiceField(
        queryset=ObjectType.objects.with_feature("tags"), required=False, label=_("Tagged object type")
    )
    for_object_type_id = ContentTypeChoiceField(
        queryset=ObjectType.objects.with_feature("tags"), required=False, label=_("Allowed object type")
    )

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Tag",
                "content_type_id",
                "for_object_type_id",
            ),
        )
        return helper


class ObjectChangeFilterForm(PrimaryModelFilterSetForm):
    model = ObjectChange
    time_after = forms.DateTimeField(required=False, label=_("After"))
    time_before = forms.DateTimeField(required=False, label=_("Before"))
    action = forms.ChoiceField(label=_("Action"), choices=add_blank_choice(ObjectChangeActionChoices), required=False)
    user_id = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label=_("User"))
    changed_object_type_id = ContentTypeMultipleChoiceField(
        queryset=ObjectType.objects.with_feature("change_logging"),
        required=False,
        label=_("Object Type"),
    )

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Time",
                DateTime("time_before"),
                DateTime("time_after"),
            )
        )
        helper.layout.append(
            Fieldset(
                "Attributes",
                "action",
                "user_id",
                "changed_object_type_id",
            )
        )
        return helper


class CustomFieldChoiceSetFilterForm(PrimaryModelFilterSetForm):
    model = CustomFieldChoiceSet
    choice = forms.CharField(required=False)

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Choices",
                "choice",
            )
        )

        return helper
