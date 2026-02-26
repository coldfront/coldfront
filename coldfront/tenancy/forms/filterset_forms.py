# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import NestedGroupModelFilterSetForm, PrimaryModelFilterSetForm
from coldfront.tenancy.models import Tenant, TenantGroup
from coldfront.utils.forms.fields import TagFilterField


class TenantGroupFilterSetForm(NestedGroupModelFilterSetForm):
    model = TenantGroup
    parent_id = forms.ModelChoiceField(queryset=TenantGroup.objects.all(), required=False, label=_("Parent Group"))
    tag = TagFilterField(model)

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Tenant Group",
                "parent_id",
                "tag",
            ),
        )
        return helper


class TenantFilterSetForm(PrimaryModelFilterSetForm):
    model = Tenant
    group_id = forms.ModelChoiceField(queryset=TenantGroup.objects.all(), required=False, label=_("Tenant Group"))
    tag = TagFilterField(model)

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Tenant",
                "group_id",
                "tag",
            ),
        )
        return helper


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
