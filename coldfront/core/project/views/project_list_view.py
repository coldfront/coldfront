# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from coldfront.core.project.forms import ProjectSearchForm
from coldfront.core.project.models import Project
from coldfront.core.project.utils import (
    form_data_to_query_string,
    handle_pagination,
    handle_sorting_params,
    project_list_query,
    project_list_query_default,
    sort_params_to_query_string,
)

logger = logging.getLogger(__name__)


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project/project_list.html"
    context_object_name = "project_list"
    paginate_by = 25
    project_status_choices = ["New", "Active"]

    def get_queryset(self):
        order_by = handle_sorting_params(
            self.request.GET.get("order_by", "id"), self.request.GET.get("direction", "asc")
        )

        project_search_form = ProjectSearchForm(self.request.GET)
        if project_search_form.is_valid():
            data = project_search_form.cleaned_data
            show_all = data.get("show_all_projects") and (
                self.request.user.is_superuser or self.request.user.has_perm("project.can_view_all_projects")
            )
            return project_list_query(data, self.request.user, order_by, self.project_status_choices, show_all=show_all)

        else:
            return project_list_query_default(self.request.user, order_by, self.project_status_choices)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects_count"] = self.get_queryset().count()

        handle_pagination(self.request.GET.get("page"), context.get("project_list"), self.paginate_by)

        # Add the project search form to the context
        return self.add_project_search_form_context(context, self.request)

    def add_project_search_form_context(self, context, request):
        project_search_form = ProjectSearchForm(request.GET)
        filter_parameters = ""
        if project_search_form.is_valid():
            data = project_search_form.cleaned_data
            # Convert form data to query string
            filter_parameters = form_data_to_query_string(data)

            context["project_search_form"] = project_search_form
        else:
            context["project_search_form"] = ProjectSearchForm()

        context["filter_parameters"] = filter_parameters
        context["filter_parameters_with_order_by"] = filter_parameters + self.add_sort_params(request)

        if filter_parameters:
            context["expand_accordion"] = "show"

        return context

    def add_sort_params(self, request):
        order_by = request.GET.get("order_by")
        if order_by:
            direction = request.GET.get("direction")
            return sort_params_to_query_string(order_by, direction)
        return ""
