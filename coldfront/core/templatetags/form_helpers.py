# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django import template

register = template.Library()


@register.filter()
def getfield(form, fieldname):
    """
    Return the specified bound field of a Form.
    """
    try:
        return form[fieldname]
    except KeyError:
        return None


@register.filter(name="widget_type")
def widget_type(field):
    """
    Return the widget type
    """
    if hasattr(field, "widget"):
        return field.widget.__class__.__name__.lower()
    if hasattr(field, "field"):
        return field.field.widget.__class__.__name__.lower()
    return None


@register.inclusion_tag("helpers/render_field.html")
def render_field(field, bulk_nullable=False, label=None):
    """
    Render a single form field from template
    """
    return {
        "field": field,
        "label": label or field.label,
        "bulk_nullable": bulk_nullable or getattr(field, "_nullable", False),
    }
