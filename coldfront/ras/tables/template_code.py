# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

ALLOCATIONTYPE_ATTRIBUTES = """
{% if value %}{% for attr in value %}{{ attr }}{% if not forloop.last %}, {% endif %}{% endfor %}{% endif %}
"""

ALLOCATION_RESOURCES = """
{% load helpers %}
{% for r in value.all %}
<span class="badge" style="color: {{ r.resource_type.color|fgcolor }}; background-color: #{{ r.resource_type.color }}">
<a href="{{ r.get_absolute_url }}">{{ r }}</a>
</span>
{% endfor %}
"""
