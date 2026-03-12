# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import NestedGroupModelFilterSetForm, PrimaryModelFilterSetForm
from coldfront.forms.fields import TagFilterField
from coldfront.tenancy.models import Tenant, TenantGroup


class TenantGroupFilterSetForm(NestedGroupModelFilterSetForm):
    model = TenantGroup
    parent_id = forms.ModelChoiceField(queryset=TenantGroup.objects.all(), required=False, label=_("Parent Group"))
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            "Tenant Group",
            "parent_id",
            "tag",
        ),
    )


class TenantFilterSetForm(PrimaryModelFilterSetForm):
    model = Tenant
    group_id = forms.ModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_("Tenant Group"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            "Tenant",
            "group_id",
            "tag",
        ),
    )


class TenancyFilterSetForm(forms.Form):
    tenant_group_id = forms.ModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_("Tenant group"),
    )
    tenant_id = forms.ModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_("Tenant"),
    )
