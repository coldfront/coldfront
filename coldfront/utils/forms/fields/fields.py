# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import json

from django import forms
from django.conf import settings
from django.db.models import Count
from django.forms.fields import InvalidJSONInput
from django.forms.fields import JSONField as _JSONField
from django.utils.translation import gettext_lazy as _


class QueryField(forms.CharField):
    """
    A CharField subclass used for global search/query fields in filter forms.
    """

    pass


class SlugField(forms.SlugField):
    """
    Extend Django's built-in SlugField to automatically populate from a field called `name` unless otherwise specified.

    Parameters:
        slug_source: Name of the form field from which the slug value will be derived
    """

    label = _("Slug")
    help_text = _("URL-friendly unique shorthand")

    def __init__(self, *, slug_source="name", label=label, help_text=help_text, **kwargs):
        super().__init__(label=label, help_text=help_text, **kwargs)

        self.slug_source = slug_source

    def get_bound_field(self, form, field_name):
        if prefix := form.prefix:
            if self.slug_source and not self.slug_source.startswith(f"{prefix}-"):
                self.slug_source = f"{prefix}-{self.slug_source}"

        return super().get_bound_field(form, field_name)


class TagFilterField(forms.MultipleChoiceField):
    """
    A filter field for the tags of a model. Only the tags used by a model are displayed.

    :param model: The model of the filter
    """

    def __init__(self, model, *args, **kwargs):
        def get_choices():
            tags = model.tags.annotate(count=Count("core_taggeditem_items")).order_by("name")
            return [
                (settings.FILTERS_NULL_CHOICE_VALUE, settings.FILTERS_NULL_CHOICE_LABEL),  # "None" option
                *[(str(tag.slug), f"{tag.name} ({tag.count})") for tag in tags],
            ]

        # Choices are fetched each time the form is initialized
        super().__init__(label=_("Tags"), choices=get_choices, required=False, *args, **kwargs)


class JSONField(_JSONField):
    """
    Custom wrapper around Django's built-in JSONField to avoid presenting "null" as the default text.
    """

    empty_values = [None, "", ()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget.attrs["placeholder"] = ""
        self.widget.attrs["class"] = "font-monospace"
        if not self.help_text:
            self.help_text = _('Enter context data in <a href="https://json.org/">JSON</a> format.')

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        if value in ("", None):
            return ""
        if type(value) is str:
            try:
                value = json.loads(value, cls=self.decoder)
            except json.decoder.JSONDecodeError:
                return f'"{value}"'
        return json.dumps(value, sort_keys=True, indent=4, ensure_ascii=False, cls=self.encoder)
