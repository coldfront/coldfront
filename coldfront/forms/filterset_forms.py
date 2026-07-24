# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from .mixins import HorizontalFormMixin, SavedFiltersMixin

__all__ = (
    "ColdFrontModelFilterSetForm",
    "PrimaryModelFilterSetForm",
    "OrganizationalModelFilterSetForm",
    "NestedGroupModelFilterSetForm",
)


class BaseModelFilterSetForm(SavedFiltersMixin, HorizontalFormMixin, forms.Form):
    """
    Base form for FilerSet forms. These are used to filter object lists in the ColdFront UI. Note that the
    corresponding FilterSet *must* provide a `q` filter.
    """

    q = forms.CharField(required=False, label=_("Search"))
    selector_fields = ("filter_id", "q")
    fieldsets = ()

    @property
    def helper(self):
        """
        crispy forms helper which defines the form rendering behavior. Override to set form method to get
        """
        helper = super().helper
        helper.form_method = "get"
        return helper

    def get_layout(self):
        """
        Override crispy layout to include search and filter fields
        """
        fieldsets = [Fieldset(_("Search"), "q", "filter_id"), *self.fieldsets]

        return Layout(*fieldsets)


class ColdFrontModelFilterSetForm(BaseModelFilterSetForm):
    """
    Base form for FilterSet forms.
    """

    pass


class PrimaryModelFilterSetForm(ColdFrontModelFilterSetForm):
    """
    FilterSet form for models which inherit from PrimaryModel.
    """

    pass


class OrganizationalModelFilterSetForm(ColdFrontModelFilterSetForm):
    """
    FilterSet form for models which inherit from OrganizationalModel.
    """

    pass


class NestedGroupModelFilterSetForm(ColdFrontModelFilterSetForm):
    """
    FilterSet form for models which inherit from NestedGroupModel.
    """

    pass
