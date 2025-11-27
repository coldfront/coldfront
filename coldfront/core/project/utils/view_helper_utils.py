# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from coldfront.core.allocation.utils import generate_guauge_data_from_usage
from coldfront.core.project.models import Project, ProjectUserRoleChoice
from coldfront.core.user.utils import CombinedUserSearch

logger = logging.getLogger(__name__)


def user_is_pi_or_manager(user, project_obj):
    """Utility function to check if a user is PI or Manager of a project."""
    if user.is_superuser:
        return True

    if project_obj.pi == user:
        return True

    if project_obj.projectuser_set.filter(user=user, role__name="Manager", status__name="Active").exists():
        return True

    return False


def user_can_view_project(user, project_obj):
    """Utility function to check if a user can view a project."""
    if user.is_superuser:
        return True

    if user.has_perm("project.can_view_all_projects"):
        return True

    if project_obj.projectuser_set.filter(user=user, status__name="Active").exists():
        return True

    return False


def get_or_create_local_user_from_form(user_form_data):
    """Utility function to get or create a local user."""
    user_obj, _ = User.objects.get_or_create(username=user_form_data.get("username"))
    user_obj.first_name = user_form_data.get("first_name")
    user_obj.last_name = user_form_data.get("last_name")
    user_obj.email = user_form_data.get("email")
    user_obj.save()
    return user_obj


def handle_sorting_params(order_by, direction="asc"):
    if order_by != "name":
        if direction == "asc":
            direction = ""
        if direction == "des":
            direction = "-"
        order_by = direction + order_by
    return order_by


def sort_params_to_query_string(order_by, direction):
    return f"order_by={order_by}&direction={direction}"


def form_data_to_query_string(form_data):
    filter_parameters = ""
    for key, value in form_data.items():
        if value:
            if isinstance(value, list):
                for ele in value:
                    filter_parameters += f"{key}={ele}&"
            else:
                filter_parameters += f"{key}={value}&"
    return filter_parameters


def project_list_query(form_data, user, order_by: str, project_statuses: list, show_all=False):
    prefetch_related = ["status"]
    if form_data.get("field_of_science"):
        prefetch_related.append("field_of_science")
    if form_data.get("last_name") or form_data.get("username"):
        prefetch_related.append("pi")
    projects = Project.objects.prefetch_related(*prefetch_related)

    if show_all:
        projects = projects.filter(status__name__in=project_statuses)
    else:
        # only show projects the user is active in
        projects = projects.filter(
            Q(status__name__in=project_statuses) & Q(projectuser__user=user) & Q(projectuser__status__name="Active")
        )

    # title
    if form_data.get("title"):
        projects = projects.filter(title__icontains=form_data.get("title"))

    # Last Name
    if form_data.get("last_name"):
        projects = projects.filter(pi__last_name__icontains=form_data.get("last_name"))

    # Username
    if form_data.get("username"):
        projects = projects.filter(
            Q(pi__username__icontains=form_data.get("username"))
            | Q(projectuser__user__username__icontains=form_data.get("username"))
            & Q(projectuser__status__name="Active")
        )

    # Field of Science
    if form_data.get("field_of_science"):
        projects = projects.filter(field_of_science__description__icontains=form_data.get("field_of_science"))

    return projects.order_by(order_by).distinct()


def project_list_query_default(user, order_by: str, project_statuses: list = ("New", "Active")):
    return (
        Project.objects.prefetch_related(["status"])
        .filter(
            Q(status__name__in=project_statuses) & Q(projectuser__user=user) & Q(projectuser__status__name="Active")
        )
        .order_by(order_by)
        .distinct()
    )


def handle_pagination(page, item_list, items_per_page) -> None:
    """Utility function to handle pagination of model instance lists."""
    paginator = Paginator(item_list, items_per_page)

    try:
        item_list = paginator.page(page)
    except PageNotAnInteger:
        item_list = paginator.page(1)
    except EmptyPage:
        item_list = paginator.page(paginator.num_pages)


def get_project_user_search_results(project_obj, user_search_string, search_by):
    """Utility function to handle projectuser search and return context."""
    # exclude users already in the project
    users_to_exclude = [ele.user.username for ele in project_obj.projectuser_set.filter(status__name="Active")]

    result = CombinedUserSearch(user_search_string, search_by, users_to_exclude).search()

    for match in result.get("matches"):
        # default role to 'User' when adding to project
        match.update({"role": ProjectUserRoleChoice.objects.get(name="User")})

    # generate a list of users already in the project that match the search string
    if len(user_search_string.split()) > 1:
        users_already_in_project = []
        for ele in user_search_string.split():
            if ele in result["users_already_in_project"]:
                users_already_in_project.append(ele)
        result["users_already_in_project"] = users_already_in_project

    return result


def get_project_allocations_data(project_obj):
    """Utility function to get project allocations data."""
    allocation_objs = project_obj.allocation_set.filter(
        resources__is_allocatable=True,
        is_locked=False,
        status__name__in=["Active", "New", "Renewal Requested", "Payment Pending", "Payment Requested", "Paid"],
    )
    return [
        {
            "pk": allocation_obj.pk,
            "resource": allocation_obj.get_parent_resource.name,
            "details": allocation_obj.get_information,
            "resource_type": allocation_obj.get_parent_resource.resource_type.name,
            "status": allocation_obj.status.name,
        }
        for allocation_obj in allocation_objs
    ]


def project_attribute_with_usage_to_gauge(attribute):
    """Convert a project attribute with usage to gauge data."""
    try:
        return generate_guauge_data_from_usage(
            attribute.proj_attr_type.name,
            float(attribute.value),
            float(attribute.projectattributeusage.value),
        )
    except ValueError:
        logger.error("Project attribute '%s' is not an int but has a usage", attribute.proj_attr_type.name)
        return None
