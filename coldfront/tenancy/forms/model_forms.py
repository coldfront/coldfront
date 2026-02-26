# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from crispy_forms.layout import Field, Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import NestedGroupModelForm
from coldfront.forms.layouts import Slug
from coldfront.tenancy.models import Tenant, TenantGroup
from coldfront.utils.forms.fields import SlugField

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

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Tenant Group",
                Field("parent"),
                Field("name"),
                Slug(),
                Field("description"),
                Field("tags"),
            )
        )

        return helper


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

    @property
    def helper(self):
        helper = super().helper
        helper.layout.append(
            Fieldset(
                "Tenant",
                Field("name"),
                Slug(),
                Field("group"),
                Field("description"),
                Field("tags"),
            )
        )

        return helper


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
