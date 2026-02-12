# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


# settings value
@register.simple_tag
def settings_value(name):
    allowed_names = [
        "LOGIN_FAIL_MESSAGE",
        "ACCOUNT_CREATION_TEXT",
        "CENTER_NAME",
        "CENTER_HELP_URL",
        "EMAIL_PROJECT_REVIEW_CONTACT",
    ]
    # FIXME: This is using mark_safe for now but settings should not contain HTML in the future
    return mark_safe(getattr(settings, name, "") if name in allowed_names else "")  # noqa: S308


@register.filter
def get_icon(expand_accordion):
    if expand_accordion == "show":
        return "fa-minus"
    else:
        return "fa-plus"


@register.filter
def convert_boolean_to_icon(boolean):
    if boolean is False:
        return mark_safe('<span class="badge bg-success"><i class="fas fa-check"></i></span>')
    else:
        return mark_safe('<span class="badge bg-danger"><i class="fas fa-times"></i></span>')


@register.filter
def convert_status_to_icon(project):
    last_project_review = project.last_project_review
    needs_review = project.needs_review
    if last_project_review:
        status = last_project_review.status.name
        if status == "Pending":
            return mark_safe('<h4><span class="badge bg-info"><i class="fas fa-exclamation-circle"></i></span></h4>')
        elif status == "Completed":
            return mark_safe('<h4><span class="badge bg-success"><i class="fas fa-check-circle"></i></span></h4>')
    elif needs_review and not last_project_review:
        return mark_safe('<h4><span class="badge bg-danger"><i class="fas fa-question-circle"></i></span></h4>')
    elif not needs_review:
        return mark_safe('<h4><span class="badge bg-success"><i class="fas fa-check-circle"></i></span></h4>')


@register.filter("get_value_from_dict")
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)


@register.filter("get_value_by_index")
def get_value_by_index(array, index):
    """
    usage example {{ your_list|get_value_by_index:your_index }}
    """
    return array[index]


@register.simple_tag
def navbar_active_item(menu_item, request):
    view_map = {
        "center-summary": ["center-summary"],
        "home": ["home"],
        "invoice": ["allocation-invoice-list"],
        "project": ["project-list", "allocation-list", "allocation-account-list", "resource-list"],
        "admin": [
            "user-search-home",
            "project-review-list",
            "allocation-request-list",
            "allocation-change-list",
            "grant-report",
        ],
        "staff": [
            "user-search-home",
            "project-review-list",
            "allocation-request-list",
            "grant-report",
        ],
        "director": [
            "project-review-list",
            "grant-report",
        ],
    }
    if request.resolver_match is not None:
        view_name = request.resolver_match.view_name
        if menu_item in view_map:
            if view_name in view_map[menu_item]:
                return "active"
    return ""
