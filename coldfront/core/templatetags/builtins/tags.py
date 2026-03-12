# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django import template

from coldfront.core.choices import CustomFieldTypeChoices
from coldfront.core.utils import ActionURLNode
from coldfront.forms import TableConfigForm

register = template.Library()


@register.inclusion_tag("builtins/customfield_value.html")
def customfield_value(customfield, value):
    """
    Render a custom field value according to the field type.

    Args:
        customfield: A CustomField instance
        value: The custom field value applied to an object
    """
    if value:
        if customfield.type == CustomFieldTypeChoices.TYPE_SELECT:
            value = customfield.get_choice_label(value)
        elif customfield.type == CustomFieldTypeChoices.TYPE_MULTISELECT:
            value = [customfield.get_choice_label(v) for v in value]
    return {
        "customfield": customfield,
        "value": value,
    }


@register.inclusion_tag("builtins/table_config_form.html")
def table_config_form(table, table_name=None):
    return {
        "table_name": table_name or table.__class__.__name__,
        "form": TableConfigForm(table=table),
    }


@register.tag
def action_url(parser, token):
    """
    Return an absolute URL matching the given model and action.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% action_url model "action_name" %}

        or

        {% action_url model "action_name" pk=object.pk %}

        or

        {% action_url model "action_name" pk=object.pk as variable_name %}

    The first argument is a model or instance. The second argument is the action name.
    Additional keyword arguments can be passed for URL parameters.

    For example, if you have a Device model and want to link to its edit action::

        {% action_url device "edit" %}
        This will generate a URL like ``/dcim/devices/123/edit/``.

        You can also pass additional parameters::

            {% action_url device "journal" pk=device.pk %}

        Or assign the URL to a variable::

            {% action_url device "edit" as edit_url %}
    """

    # Parse the token contents
    bits = token.split_contents()
    if len(bits) < 3:
        raise template.TemplateSyntaxError(f"'{bits[0]}' takes at least two arguments, a model and an action.")

    # Extract model and action
    model = parser.compile_filter(bits[1])
    action = bits[2].strip("\"'")  # Remove quotes from literal string
    kwargs = {}
    asvar = None
    bits = bits[3:]

    # Handle 'as' syntax for variable assignment
    if len(bits) >= 2 and bits[-2] == "as":
        asvar = bits[-1]
        bits = bits[:-2]

    # Parse remaining arguments as kwargs
    for bit in bits:
        if "=" not in bit:
            raise template.TemplateSyntaxError(
                f"'{token.contents.split()[0]}' keyword arguments must be in the format 'name=value'"
            )
        name, value = bit.split("=", 1)
        kwargs[name] = parser.compile_filter(value)

    return ActionURLNode(model, action, kwargs, asvar)


@register.simple_tag()
def qstring_update(request, **kwargs):
    """
    Append or update the page number in a querystring.
    """
    querydict = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            querydict[k] = str(v)
        elif k in querydict:
            querydict.pop(k)
    querystring = querydict.urlencode(safe="/")
    if querystring:
        return "?" + querystring
    else:
        return ""
