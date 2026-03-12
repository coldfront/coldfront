# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django import template
from django.utils.html import format_html

__all__ = ("action_buttons",)

register = template.Library()


@register.simple_tag(takes_context=True)
def action_buttons(context, actions, obj, multi=False, **kwargs):
    buttons = [action.render(context, obj, **kwargs) for action in actions if action.multi == multi]
    return format_html("".join(buttons))
