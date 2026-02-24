# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django import forms
from django.contrib.contenttypes.models import ContentType

from coldfront.utils.forms.fields import SlugField

from .mixins import ChangelogMessageMixin, CheckLastUpdatedMixin, CustomFieldsMixin, HorizontalFormMixin, TagsMixin

__all__ = (
    "NestedGroupModelForm",
    "ColdFrontModelForm",
    "OrganizationalModelForm",
    "PrimaryModelForm",
)


class ColdFrontModelForm(
    ChangelogMessageMixin,
    CheckLastUpdatedMixin,
    CustomFieldsMixin,
    TagsMixin,
    HorizontalFormMixin,
    forms.ModelForm,
):
    """
    Base form for creating & editing ColdFront models.
    """

    def _get_content_type(self):
        return ContentType.objects.get_for_model(self._meta.model)

    def _post_clean(self):
        """
        Override BaseModelForm's _post_clean() to store many-to-many field values on the model instance.
        """
        self.instance._m2m_values = {}
        for field in self.instance._meta.local_many_to_many:
            if field.name in self.cleaned_data:
                self.instance._m2m_values[field.name] = list(self.cleaned_data[field.name])

        return super()._post_clean()

    def _get_form_field(self, customfield):
        if self.instance.pk:
            form_field = customfield.to_form_field(set_initial=False)
            form_field.initial = self.instance.custom_field_data.get(customfield.name)
            return form_field

        return customfield.to_form_field()

    def clean(self):

        # Save custom field data on instance
        for cf_name, customfield in self.custom_fields.items():
            if cf_name not in self.fields:
                # Custom fields may be absent when performing bulk updates via import
                continue
            key = cf_name[3:]  # Strip "cf_" from field name
            value = self.cleaned_data.get(cf_name)

            # Convert "empty" values to null
            if value in self.fields[cf_name].empty_values:
                self.instance.custom_field_data[key] = None
            else:
                self.instance.custom_field_data[key] = customfield.serialize(value)

        return super().clean()


class PrimaryModelForm(ColdFrontModelForm):
    """
    Form for models which inherit from PrimaryModel.
    """

    pass


class OrganizationalModelForm(ColdFrontModelForm):
    """
    Form for models which inherit from OrganizationalModel.
    """

    slug = SlugField()

    pass


class NestedGroupModelForm(ColdFrontModelForm):
    """
    Form for models which inherit from NestedGroupModel.
    """

    slug = SlugField()

    pass
