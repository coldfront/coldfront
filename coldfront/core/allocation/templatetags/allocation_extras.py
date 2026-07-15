# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Look up ``key`` in ``dictionary`` and return the value, or None.

    Used by allocation templates that render a per-user role cell from a
    precomputed ``user_roles_map`` keyed by username. Registered on a
    proper ``template.Library`` so it resolves at template compile time
    regardless of view-module import order.
    """
    if not dictionary:
        return None
    return dictionary.get(key)
