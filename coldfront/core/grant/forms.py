# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django import forms
from django.forms import ModelForm

from coldfront.core.grant.models import Grant
from coldfront.core.utils.common import import_from_settings

CENTER_NAME = import_from_settings("CENTER_NAME")


class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = [
            "project",
        ]
        labels = {
            "percent_credit": f"Percent credit to {CENTER_NAME}",
            "direct_funding": f"Direct funding to {CENTER_NAME}",
        }
        help_texts = {
            "percent_credit": f"Percent financial credit of the total grant amount to {CENTER_NAME}.",
            "direct_funding": f"Funds budgeted specifically for {CENTER_NAME} services, hardware, software, and/or personnel.",
        }

    def __init__(self, *args, **kwargs):
        super(GrantForm, self).__init__(*args, **kwargs)
        self.fields["funding_agency"].queryset = self.fields["funding_agency"].queryset.order_by("name")
        self.fields["grant_start"].widget.attrs["class"] = "datepicker"
        self.fields["grant_end"].widget.attrs["class"] = "datepicker"
        self.fields["direct_funding"].widget.widgets[0].attrs["step"] = "0.01"
        self.fields["total_amount_awarded"].widget.widgets[0].attrs["step"] = "0.01"
        self.fields["direct_funding"].widget.widgets[1].attrs["class"] = "select form-select"
        self.fields["total_amount_awarded"].widget.widgets[1].attrs["class"] = "select form-select"


class GrantDeleteForm(forms.Form):
    title = forms.CharField(max_length=255, disabled=True)
    grant_number = forms.CharField(max_length=30, required=False, disabled=True)
    grant_end = forms.CharField(max_length=150, required=False, disabled=True)
    selected = forms.BooleanField(initial=False, required=False)


class GrantDownloadForm(forms.Form):
    pk = forms.IntegerField(required=False, disabled=True)
    title = forms.CharField(required=False, disabled=True)
    project_pk = forms.IntegerField(required=False, disabled=True)
    pi_first_name = forms.CharField(required=False, disabled=True)
    pi_last_name = forms.CharField(required=False, disabled=True)
    role = forms.CharField(required=False, disabled=True)
    grant_pi = forms.CharField(required=False, disabled=True)
    total_amount_awarded = forms.FloatField(required=False, disabled=True)
    funding_agency = forms.CharField(required=False, disabled=True)
    grant_number = forms.CharField(required=False, disabled=True)
    grant_start = forms.DateField(required=False, disabled=True)
    grant_end = forms.DateField(required=False, disabled=True)
    percent_credit = forms.FloatField(required=False, disabled=True)
    direct_funding = forms.FloatField(required=False, disabled=True)
    selected = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pk"].widget = forms.HiddenInput()
