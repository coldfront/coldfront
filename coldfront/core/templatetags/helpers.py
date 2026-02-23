# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from typing import Any, Dict

from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.html import conditional_escape

from coldfront.utils.forms import TableConfigForm
from coldfront.views import get_action_url, get_viewname

register = template.Library()


class ActionURLNode(template.Node):
    """Template node for the {% action_url %} template tag."""

    child_nodelists = ()

    def __init__(self, model, action, kwargs, asvar=None):
        self.model = model
        self.action = action
        self.kwargs = kwargs
        self.asvar = asvar

    def __repr__(self):
        return (
            f"<{self.__class__.__qualname__} "
            f"model='{self.model}' "
            f"action='{self.action}' "
            f"kwargs={repr(self.kwargs)} "
            f"as={repr(self.asvar)}>"
        )

    def render(self, context):
        """
        Render the action URL node.

        Args:
            context: The template context

        Returns:
            The resolved URL or empty string if using 'as' syntax

        Raises:
            NoReverseMatch: If the URL cannot be resolved and not using 'as' syntax
        """
        # Resolve model and kwargs from context
        model = self.model.resolve(context)
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}

        # Get the action URL using the utility function
        try:
            url = get_action_url(model, action=self.action, kwargs=kwargs)
        except NoReverseMatch:
            if self.asvar is None:
                raise
            url = ""

        # Handle variable assignment or return escaped URL
        if self.asvar:
            context[self.asvar] = url
            return ""

        return conditional_escape(url) if context.autoescape else url


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
def querystring(request, **kwargs):
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


@register.filter
def get_key(value: Dict, arg: str) -> Any:
    """
    Template implementation of `dict.get()`, for accessing dict values
    by key when the key is not able to be used in a template. For
    example, `{"ui.colormode": "dark"}`.
    """
    return value.get(arg, None)


@register.filter()
def validated_viewname(model, action):
    """
    Return the view name for the given model and action if valid, or None if invalid.
    """
    viewname = get_viewname(model, action)

    # Validate the view name
    try:
        reverse(viewname)
        return viewname
    except NoReverseMatch:
        return None


@register.inclusion_tag("helpers/table_config_form.html")
def table_config_form(table, table_name=None):
    return {
        "table_name": table_name or table.__class__.__name__,
        "form": TableConfigForm(table=table),
    }
