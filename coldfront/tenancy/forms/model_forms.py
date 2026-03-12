# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import NestedGroupModelForm
from coldfront.forms.fields import SlugField
from coldfront.forms.layouts import Slug
from coldfront.tenancy.models import Tenant, TenantGroup

__all__ = ("TenantGroupForm", "TenantForm")


class TenantGroupForm(NestedGroupModelForm):
    class Meta:
        model = TenantGroup
        fields = [
            "parent",
            "name",
            "slug",
            "description",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            "Tenant Group",
            "parent",
            "name",
            Slug(),
            "description",
            "tags",
        ),
    )


class TenantForm(NestedGroupModelForm):
    slug = SlugField()

    class Meta:
        model = Tenant
        fields = [
            "name",
            "slug",
            "group",
            "description",
            "tags",
        ]

    fieldsets = (
        Fieldset(
            "Tenant",
            "name",
            Slug("slug"),
            "group",
            "description",
            "tags",
        ),
    )


class TenancyForm(forms.Form):
    tenant_group = forms.ModelChoiceField(
        label=_("Tenant group"),
        queryset=TenantGroup.objects.all(),
        required=False,
    )
    tenant = forms.ModelChoiceField(
        label=_("Tenant"),
        queryset=Tenant.objects.all(),
        required=False,
    )
