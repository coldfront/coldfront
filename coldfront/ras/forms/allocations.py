# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelForm, PrimaryModelForm
from coldfront.forms.layouts import DateTime
from coldfront.forms.mixins import AttributeProfileForm, CustomAttributesMixin
from coldfront.forms.widgets import HTMXSelect
from coldfront.ras.models import Allocation, AllocationType
from coldfront.tenancy.forms import TenancyForm


class AllocationForm(TenancyForm, CustomAttributesMixin, PrimaryModelForm):
    allocation_type = forms.ModelChoiceField(
        queryset=AllocationType.objects.all(),
        label=_("Allocation Type"),
        required=False,
        widget=HTMXSelect(),
    )

    profile_field_name = "allocation_type"

    class Meta:
        model = Allocation
        fields = [
            "allocation_type",
            "project",
            "resources",
            "owner",
            "start_date",
            "end_date",
            "status",
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
                _("Allocation"),
                "project",
                "resources",
                "owner",
                DateTime("start_date"),
                DateTime("end_date"),
                "status",
                "description",
                "justification",
                "tags",
            ),
            Fieldset(
                "Allocation Type",
                "allocation_type",
                *self.attr_fields,
            ),
            Fieldset(
                _("Tenant"),
                "tenant_group",
                "tenant",
            ),
        ]


class AllocationTypeForm(AttributeProfileForm, OrganizationalModelForm):
    class Meta:
        model = AllocationType
        fields = [
            "name",
            "schema",
            "description",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            _("Allocation Type"),
            "name",
            "description",
            "schema",
            "tags",
        ),
    )
