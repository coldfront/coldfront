# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from coldfront.core.project.forms import (
    ProjectAddUserForm,
    ProjectAddUsersToAllocationForm,
)
from coldfront.core.project.models import Project
from coldfront.core.project.utils import (
    get_project_allocations_data,
    get_project_user_search_results,
    project_is_archived,
    user_is_pi_or_manager,
)
from coldfront.core.user.forms import UserSearchForm

logger = logging.getLogger(__name__)


class ProjectAddUsersSearchView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_add_users.html"

    def test_func(self):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return user_is_pi_or_manager(self.request.user, project_obj)

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        if project_is_archived(project_obj):
            messages.error(request, "You cannot add users to an archived project.")
            return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["user_search_form"] = UserSearchForm()
        context["project"] = Project.objects.get(pk=self.kwargs.get("pk"))
        return context


class ProjectAddUsersSearchResultsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/add_user_search_results.html"
    raise_exception = True

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return user_is_pi_or_manager(self.request.user, project_obj)

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        if project_is_archived(project_obj):
            messages.error(request, "You cannot add users to an archived project.")
            return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_search_string = request.POST.get("q")
        search_by = request.POST.get("search_by")
        pk = self.kwargs.get("pk")

        project_obj = get_object_or_404(Project, pk=pk)
        context = get_project_user_search_results(project_obj, user_search_string, search_by)

        matches = context.get("matches")

        if matches:
            formset = formset_factory(ProjectAddUserForm, max_num=len(matches))
            formset = formset(initial=matches, prefix="userform")
            context["formset"] = formset
            context["user_search_string"] = user_search_string
            context["search_by"] = search_by

        initial_data = get_project_allocations_data(project_obj)

        allocation_formset = formset_factory(ProjectAddUsersToAllocationForm, max_num=len(initial_data))
        allocation_formset = allocation_formset(initial=initial_data, prefix="allocationform")
        context["allocation_formset"] = allocation_formset

        # The following block of code is used to hide/show the allocation div in the form.
        if project_obj.allocation_set.filter(status__name__in=["Active", "New", "Renewal Requested"]).exists():
            div_allocation_class = "placeholder_div_class"
        else:
            div_allocation_class = "d-none"
        context["div_allocation_class"] = div_allocation_class
        ###

        context["pk"] = pk
        return render(request, self.template_name, context)
