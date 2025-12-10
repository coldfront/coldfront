# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView

from coldfront.core.project.forms import ProjectRemoveUserForm
from coldfront.core.project.models import Project


class ProjectRemoveUsersView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_remove_users.html"

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
            messages.error(request, "You cannot remove users from an archived project.")
            return redirect(project_obj)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_users_to_remove(self, project_obj):
        users_to_remove = [
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

        return users_to_remove

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
                    remove_users_count += 1

                    user_obj = User.objects.get(username=user_form_data.get("username"))

                    if project_obj.pi == user_obj:
                        continue

                    project_obj.remove_user(user_obj, signal_sender=self.__class__)

            if remove_users_count == 1:
                messages.success(request, "Removed {} user from project.".format(remove_users_count))
            else:
                messages.success(request, "Removed {} users from project.".format(remove_users_count))
        else:
            for error in formset.errors:
                messages.error(request, error)

        return redirect(project_obj)
