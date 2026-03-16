# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import NestedGroupModelForm
from coldfront.forms.fields import DynamicModelChoiceField, SlugField
from coldfront.forms.layouts import Slug
from coldfront.tenancy.models import Tenant, TenantGroup

__all__ = ("TenantGroupForm", "TenantForm")


class TenantGroupForm(NestedGroupModelForm):
    parent = DynamicModelChoiceField(
        label=_("Parent"),
        queryset=TenantGroup.objects.all(),
        required=False,
    )

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
    group = DynamicModelChoiceField(
        label=_("Group"),
        queryset=TenantGroup.objects.all(),
        required=False,
    )

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
            Slug(),
            "group",
            "description",
            "tags",
        ),
    )


class TenancyForm(forms.Form):
    tenant_group = DynamicModelChoiceField(
        label=_("Tenant Group"),
        queryset=TenantGroup.objects.all(),
        required=False,
    )
    tenant = DynamicModelChoiceField(
        label=_("Tenant"),
        queryset=Tenant.objects.all(),
        required=False,
        quick_add=True,
    )
