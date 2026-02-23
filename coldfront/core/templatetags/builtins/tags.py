# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django import template

from coldfront.utils.querydict import dict_to_querydict

register = template.Library()


@register.inclusion_tag("builtins/htmx_table.html", takes_context=True)
def htmx_table(context, viewname, return_url=None, **kwargs):
    """
    Embed an object list table retrieved using HTMX. Any extra keyword arguments are passed as URL query parameters.

    Args:
        context: The current request context
        viewname: The name of the view to use for the HTMX request (e.g. `dcim:site_list`)
        return_url: The URL to pass as the `return_url`. If not provided, the current request's path will be used.
    """
    url_params = dict_to_querydict(kwargs)
    url_params["return_url"] = return_url or context["request"].path
    return {
        "viewname": viewname,
        "url_params": url_params,
    }


@register.inclusion_tag("builtins/tag.html")
def tag(value, viewname=None):
    """
    Display a tag, optionally linked to a filtered list of objects.

    Args:
        value: A Tag instance
        viewname: If provided, the tag will be a hyperlink to the specified view's URL
    """
    return {
        "tag": value,
        "viewname": viewname,
    }
