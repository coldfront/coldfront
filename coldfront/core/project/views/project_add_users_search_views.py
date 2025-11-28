# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView

from coldfront.core.project.forms import ProjectAddUserForm, ProjectAddUsersToAllocationForm
from coldfront.core.project.models import Project, ProjectUserRoleChoice
from coldfront.core.user.forms import UserSearchForm
from coldfront.core.user.utils import CombinedUserSearch


class ProjectAddUsersSearchView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_add_users.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if project_obj.pi == self.request.user:
            return True

        if project_obj.projectuser_set.filter(
            user=self.request.user, role__name="Manager", status__name="Active"
        ).exists():
            return True

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project.objects.select_related("status"), pk=self.kwargs.get("pk"))
        if project_obj.status.name not in [
            "Active",
            "New",
        ]:
            messages.error(request, "You cannot add users to an archived project.")
            return redirect(project_obj.pk)
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
        if self.request.user.is_superuser:
            return True

        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if project_obj.pi == self.request.user:
            return True

        if project_obj.projectuser_set.filter(
            user=self.request.user, role__name="Manager", status__name="Active"
        ).exists():
            return True

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project.objects.select_related("status"), pk=self.kwargs.get("pk"))
        if project_obj.status.name not in [
            "Active",
            "New",
        ]:
            messages.error(request, "You cannot add users to an archived project.")
            return redirect(project_obj.pk)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_initial_data(self, project_obj):
        allocation_objs = project_obj.allocation_set.select_related("status").filter(
            resources__is_allocatable=True,
            is_locked=False,
            status__name__in=["Active", "New", "Renewal Requested", "Payment Pending", "Payment Requested", "Paid"],
        )
        initial_data = []
        for allocation_obj in allocation_objs:
            resource = allocation_obj.get_parent_resource
            initial_data.append(
                {
                    "pk": allocation_obj.pk,
                    "resource": resource.name,
                    "details": allocation_obj.get_information,
                    "resource_type": resource.resource_type.name,
                    "status": allocation_obj.status.name,
                }
            )
        return initial_data

    def post(self, request, *args, **kwargs):
        user_search_string = request.POST.get("q")
        search_by = request.POST.get("search_by")
        pk = self.kwargs.get("pk")

        project_obj = get_object_or_404(Project, pk=pk)

        users_to_exclude = [
            ele.user.username
            for ele in project_obj.projectuser_set.select_related("user").filter(status__name="Active")
        ]

        cobmined_user_search_obj = CombinedUserSearch(user_search_string, search_by, users_to_exclude)

        context = cobmined_user_search_obj.search()

        matches = context.get("matches")
        user_role = ProjectUserRoleChoice.objects.get(name="User")
        for match in matches:
            match.update({"role": user_role})

        if matches:
            formset = formset_factory(ProjectAddUserForm, max_num=len(matches))
            formset = formset(initial=matches, prefix="userform")
            context["formset"] = formset
            context["user_search_string"] = user_search_string
            context["search_by"] = search_by

        if len(user_search_string.split()) > 1:
            users_already_in_project = []
            for ele in user_search_string.split():
                if ele in users_to_exclude:
                    users_already_in_project.append(ele)
            context["users_already_in_project"] = users_already_in_project

        # The following block of code is used to hide/show the allocation div in the form.
        if project_obj.allocation_set.filter(status__name__in=["Active", "New", "Renewal Requested"]).exists():
            div_allocation_class = "placeholder_div_class"
        else:
            div_allocation_class = "d-none"
        context["div_allocation_class"] = div_allocation_class
        ###

        initial_data = self.get_initial_data(project_obj)
        allocation_formset = formset_factory(ProjectAddUsersToAllocationForm, max_num=len(initial_data))
        allocation_formset = allocation_formset(initial=initial_data, prefix="allocationform")

        context["pk"] = pk
        context["allocation_formset"] = allocation_formset
        return render(request, self.template_name, context)
