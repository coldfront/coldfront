# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from coldfront.core.project.forms import ProjectRemoveUserForm
from coldfront.core.project.models import Project
from coldfront.core.project.utils import project_is_archived, remove_user_from_project, user_is_pi_or_manager


class ProjectRemoveUsersView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_remove_users.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return user_is_pi_or_manager(self.request.user, project_obj)

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        if project_is_archived(project_obj):
            messages.error(request, "You cannot remove users from an archived project.")
            return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_users_to_remove(self, project_obj):
        return [
            {
                "username": ele.user.username,
                "first_name": ele.user.first_name,
                "last_name": ele.user.last_name,
                "email": ele.user.email,
                "role": ele.role,
            }
            for ele in project_obj.projectuser_set.filter(status__name="Active").order_by("user__username")
            if ele.user != self.request.user and ele.user != project_obj.pi
        ]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        project_obj = get_object_or_404(Project, pk=pk)

        users_to_remove = self.get_users_to_remove(project_obj)
        context = {}

        if users_to_remove:
            formset = formset_factory(ProjectRemoveUserForm, max_num=len(users_to_remove))
            formset = formset(initial=users_to_remove, prefix="userform")
            context["formset"] = formset

        context["project"] = get_object_or_404(Project, pk=pk)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        project_obj = get_object_or_404(Project, pk=pk)

        users_to_remove = self.get_users_to_remove(project_obj)

        formset = formset_factory(ProjectRemoveUserForm, max_num=len(users_to_remove))
        formset = formset(request.POST, initial=users_to_remove, prefix="userform")

        remove_users_count = 0

        if formset.is_valid():
            for form in formset:
                user_form_data = form.cleaned_data
                if user_form_data["selected"]:
                    user_obj = User.objects.get(username=user_form_data.get("username"))

                    if remove_user_from_project(project_obj, user_obj, obj_class=self.__class__):
                        remove_users_count += 1

            if remove_users_count == 1:
                messages.success(request, "Removed {} user from project.".format(remove_users_count))
            else:
                messages.success(request, "Removed {} users from project.".format(remove_users_count))
        else:
            for error in formset.errors:
                messages.error(request, error)

        return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": pk}))
