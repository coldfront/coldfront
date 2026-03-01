# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.constants import BOOLEAN_WITH_BLANK_CHOICES
from coldfront.forms import ColdFrontModelFilterSetForm
from coldfront.users.models import Group, ObjectPermission, User


class GroupFilterSetForm(ColdFrontModelFilterSetForm):
    model = Group
    fieldsets = (
        Fieldset(
            "q",
        ),
    )


class UserFilterSetForm(ColdFrontModelFilterSetForm):
    model = User
    fieldsets = (
        Fieldset(
            _("Search"),
            "q",
        ),
        Fieldset(
            _("Group"),
            "group_id",
        ),
        Fieldset(
            _("Status"),
            "is_active",
            "is_superuser",
        ),
    )
    group_id = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label=_("Group"),
    )
    is_active = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Is Active"),
    )
    is_superuser = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Is Superuser"),
    )


class ObjectPermissionFilterSetForm(ColdFrontModelFilterSetForm):
    model = ObjectPermission
    fieldsets = (
        Fieldset(
            _("Search"),
            "q",
        ),
        Fieldset(
            _("Permission"),
            "enabled",
            "group_id",
            "user_id",
        ),
        Fieldset(
            _("Actions"),
            "can_view",
            "can_add",
            "can_change",
            "can_delete",
        ),
    )
    enabled = forms.NullBooleanField(
        label=_("Enabled"), required=False, widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )
    group_id = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label=_("Group"),
    )
    user_id = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("User"),
    )
    can_view = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Can View"),
    )
    can_add = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Can Add"),
    )
    can_change = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Can Change"),
    )
    can_delete = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Can Delete"),
    )
