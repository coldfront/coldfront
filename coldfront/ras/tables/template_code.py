# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

CUSTOM_ATTRIBUTES = """
{% if value %}{% for attr in value %}{{ attr }}{% if not forloop.last %}, {% endif %}{% endfor %}{% endif %}
"""

RESOURCES_LIST = """
{% for r in value.all %}
<span class="badge" style="color: {{ r.resource_type.color|fgcolor }}; background-color: #{{ r.resource_type.color }}">
<a href="{{ r.get_absolute_url }}">{{ r }}</a>
</span>
{% empty %}
{{ ""|placeholder }}
{% endfor %}
"""

ALLOCATION_STATUS_ACTIONS = """
{% load i18n %}
{% if perms.ras.approve_allocation and "approve" in record.get_outgoing_transitions %}
{% cotton button.approve url="{% url 'ras:allocation_approve' pk=record.pk %}?return_url={% url 'ras:allocation_list' %}" title="{% trans 'Approve' %}" :small="True" type="link" /%}
{% endif %}
{% if perms.ras.deny_allocation and "deny" in record.get_outgoing_transitions %}
{% cotton button.deny url="{% url 'ras:allocation_approve' pk=record.pk %}?return_url={% url 'ras:allocation_list' %}" title="{% trans 'Deny' %}" :small="True" type="link" /%}
{% endif %}
"""
