# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from coldfront.core.allocation.models import Allocation
from coldfront.core.project.forms import ProjectAddUserForm, ProjectAddUsersToAllocationForm
from coldfront.core.project.models import Project, ProjectUserRoleChoice
from coldfront.core.user.utils import CombinedUserSearch


class ProjectAddUsersView(LoginRequiredMixin, UserPassesTestMixin, View):
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
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
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

        users_to_exclude = [ele.user.username for ele in project_obj.projectuser_set.filter(status__name="Active")]

        cobmined_user_search_obj = CombinedUserSearch(user_search_string, search_by, users_to_exclude)

        context = cobmined_user_search_obj.search()

        matches = context.get("matches")
        project_user_role = ProjectUserRoleChoice.objects.get(name="User")
        for match in matches:
            match.update({"role": project_user_role})

        formset = formset_factory(ProjectAddUserForm, max_num=len(matches))
        formset = formset(request.POST, initial=matches, prefix="userform")

        initial_data = self.get_initial_data(project_obj)
        allocation_formset = formset_factory(
            ProjectAddUsersToAllocationForm,
            max_num=len(initial_data),
        )
        allocation_formset = allocation_formset(
            request.POST,
            initial=initial_data,
            prefix="allocationform",
        )

        added_users_count = 0
        if formset.is_valid() and allocation_formset.is_valid():
            allocations_selected_objs = Allocation.objects.filter(
                pk__in=[
                    allocation_form.cleaned_data.get("pk")
                    for allocation_form in allocation_formset
                    if allocation_form.cleaned_data.get("selected")
                ]
            )
            for form in formset:
                user_form_data = form.cleaned_data
                if user_form_data["selected"]:
                    added_users_count += 1

                    # Will create local copy of user if not already present in local database
                    user_obj, created = User.objects.get_or_create(username=user_form_data.get("username"))
                    if created:
                        user_obj.first_name = user_form_data.get("first_name")
                        user_obj.last_name = user_form_data.get("last_name")
                        user_obj.email = user_form_data.get("email")
                        user_obj.save()

                    role_choice = user_form_data.get("role")
                    project_obj.add_user(user_obj, role_choice, signal_sender=self.__class__)

                    for allocation in allocations_selected_objs:
                        allocation.add_user(user_obj, signal_sender=self.__class__)

            messages.success(request, "Added {} users to project.".format(added_users_count))
        else:
            if not formset.is_valid():
                for error in formset.errors:
                    messages.error(request, error)

            if not allocation_formset.is_valid():
                for error in allocation_formset.errors:
                    messages.error(request, error)

        return redirect(project_obj)
