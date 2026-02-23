# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import datetime
import json
import re

from django import template
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils.html import escape, format_html
from django.utils.timezone import localtime

from coldfront.utils.html import foreground_color

register = template.Library()


@register.filter()
def as_range(n):
    """
    Return a range of n items.
    """
    try:
        int(n)
    except TypeError:
        return list()
    return range(n)


@register.filter()
def placeholder(value):
    """
    Render a muted placeholder if the value equates to False.
    """
    if value not in ("", None):
        return value

    return format_html('<span class="text-muted">&mdash;</span>')


@register.filter()
def meta(model, attr):
    """
    Return the specified Meta attribute of a model. This is needed because Django does not permit templates
    to access attributes which begin with an underscore (e.g. _meta).

    Args:
        model: A Django model class or instance
        attr: The attribute name
    """
    return getattr(model._meta, attr, "")


@register.filter()
def linkify(instance, attr=None):
    """
    Render a hyperlink for an object with a `get_absolute_url()` method, optionally specifying the name of an
    attribute to use for the link text. If no attribute is given, the object's string representation will be
    used.

    If the object has no `get_absolute_url()` method, return the text without a hyperlink element.
    """
    if instance is None:
        return ""

    text = getattr(instance, attr) if attr is not None else str(instance)
    try:
        url = instance.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, escape(text))
    except (AttributeError, TypeError):
        return escape(text)


@register.filter()
def fgcolor(value, dark="000000", light="ffffff"):
    """
    Return black (#000000) or white (#ffffff) given an arbitrary background color in RRGGBB format. The foreground
    color with the better contrast is returned.

    Args:
        value: The background color
        dark: The foreground color to use for light backgrounds
        light: The foreground color to use for dark backgrounds
    """
    value = value.lower().strip("#")
    if not re.match("^[0-9a-f]{6}$", value):
        return ""
    return f"#{foreground_color(value, dark, light)}"


@register.filter()
def isodate(value):
    if type(value) is datetime.date:
        text = value.isoformat()
        return format_html(f'<span title="{naturalday(value)}">{text}</span>')
    elif type(value) is datetime.datetime:
        local_value = localtime(value) if value.tzinfo else value
        text = local_value.date().isoformat()
        return format_html(f'<span title="{naturaltime(value)}">{text}</span>')
    else:
        return ""


@register.filter()
def isotime(value, spec="seconds"):
    if type(value) is datetime.time:
        return value.isoformat(timespec=spec)
    if type(value) is datetime.datetime:
        local_value = localtime(value) if value.tzinfo else value
        return local_value.time().isoformat(timespec=spec)
    return ""


@register.filter()
def isodatetime(value, spec="seconds"):
    if type(value) is datetime.datetime:
        text = f"{isodate(value)} {isotime(value, spec=spec)}"
    else:
        return ""
    return format_html(f'<span title="{naturaltime(value)}">{text}</span>')


@register.filter("json")
def render_json(value):
    """
    Render a dictionary as formatted JSON. This filter is invoked as "json":

        {{ data_dict|json }}
    """
    return json.dumps(value, ensure_ascii=False, indent=4, sort_keys=True)


@register.filter(name="split")
def split(string, sep):
    """Return the string split by sep."""
    return string.split(sep)
