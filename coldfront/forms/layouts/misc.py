# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Field
from django.utils.html import format_html

__all__ = ("Slug", "Date", "DateTime", "Time")


class Date(Field):
    def __init__(self, name):
        super().__init__(name, css_class="date-picker")


class DateTime(Field):
    def __init__(self, name):
        super().__init__(name, css_class="datetime-picker")


class Time(Field):
    def __init__(self, name):
        super().__init__(name, css_class="time-picker")


class Slug(AppendedText):
    def __init__(self, name="slug", slug_source="name"):
        super().__init__(
            name,
            format_html(
                '<button id="reslug" type="button" title="Regenerate Slug" class="btn"> <i class="fa-solid fa-rotate"></i></button>'
            ),
            slug_source=slug_source,
        )
