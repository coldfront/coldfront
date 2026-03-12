# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0


from django import forms
from django.utils.translation import gettext as _

from coldfront.forms.fields import QueryField
from coldfront.models.features import ChangeLoggingMixin


class ConfirmationForm(forms.Form):
    """
    A generic confirmation form. The form is not valid unless the `confirm` field is checked.
    """

    return_url = forms.CharField(required=False, widget=forms.HiddenInput())
    confirm = forms.BooleanField(required=True, widget=forms.HiddenInput(), initial=True)


class DeleteForm(ConfirmationForm):
    """
    Confirm the deletion of an object, optionally providing a changelog message.
    """

    changelog_message = forms.CharField(required=False, max_length=200)

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide the changelog_message filed if the model doesn't support change logging
        if instance is None or not issubclass(instance._meta.model, ChangeLoggingMixin):
            self.fields.pop("changelog_message")


class FilterForm(forms.Form):
    """
    Base Form class for FilterSet forms.
    """

    q = QueryField(required=False, label=_("Search"))


class TableConfigForm(forms.Form):
    """
    Form for configuring user's table preferences.
    """

    available_columns = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 10, "class": "form-select"}),
        label=_("Available Columns"),
    )
    columns = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 10, "class": "form-select select-all"}),
        label=_("Selected Columns"),
    )

    def __init__(self, table, *args, **kwargs):
        self.table = table

        super().__init__(*args, **kwargs)

        # Initialize columns field based on table attributes
        if table:
            self.fields["available_columns"].choices = table.available_columns
            self.fields["columns"].choices = table.selected_columns

    @property
    def table_name(self):
        return self.table.__class__.__name__
