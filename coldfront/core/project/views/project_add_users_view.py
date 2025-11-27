# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from coldfront.core.allocation.models import (
    Allocation,
    AllocationUserStatusChoice,
)
from coldfront.core.project.forms import (
    ProjectAddUserForm,
    ProjectAddUsersToAllocationForm,
)
from coldfront.core.project.models import Project
from coldfront.core.project.utils import (
    add_user_to_allocation,
    add_user_to_project,
    determine_eula_status_for_allocation_user,
    get_or_create_local_user_from_form,
    get_project_allocations_data,
    get_project_user_search_results,
    project_is_archived,
    user_is_pi_or_manager,
)

logger = logging.getLogger(__name__)


class ProjectAddUsersView(LoginRequiredMixin, UserPassesTestMixin, View):
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

        formset = formset_factory(ProjectAddUserForm, max_num=len(matches))
        formset = formset(request.POST, initial=matches, prefix="userform")

        allocation_formset = self.handle_allocation_formset(request, project_obj)

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
                    # Will create local copy of user if not already present in local database
                    user_obj = get_or_create_local_user_from_form(user_form_data)

                    role_choice = user_form_data.get("role")
                    # Is the user already in the project?
                    # sends project_activate_user signal
                    add_user_to_project(project_obj, user_obj, role_choice, send_signals=True, obj_class=self.__class__)
                    added_users_count += 1

                    for allocation in allocations_selected_objs:
                        # for each allocation selected, add user to allocation if not added yet, otherwise update status

                        user_status_choice = AllocationUserStatusChoice.objects.get(name="Active")

                        # if allocation has EULA enabled, set status choice to PendingEULA
                        user_status_choice = determine_eula_status_for_allocation_user(allocation, user_obj)

                        add_user_to_allocation(
                            allocation,
                            user_obj,
                            user_status_choice=user_status_choice,
                            send_signals_on_activate=True,
                            obj_class=self.__class__,
                        )

            messages.success(request, "Added {} users to project.".format(added_users_count))
        else:
            if not formset.is_valid():
                for error in formset.errors:
                    messages.error(request, error)

            if not allocation_formset.is_valid():
                for error in allocation_formset.errors:
                    messages.error(request, error)

        return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": pk}))

    def handle_allocation_formset(self, request, project_obj):
        initial_data = get_project_allocations_data(project_obj)

        allocation_formset = formset_factory(
            ProjectAddUsersToAllocationForm,
            max_num=len(initial_data),
        )
        allocation_formset = allocation_formset(
            request.POST,
            initial=initial_data,
            prefix="allocationform",
        )
        return allocation_formset
