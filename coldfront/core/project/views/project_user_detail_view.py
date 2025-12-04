# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from coldfront.core.project.forms import ProjectUserUpdateForm
from coldfront.core.project.models import Project, ProjectUser, ProjectUserRoleChoice


class ProjectUserDetail(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_user_detail.html"

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

    def get(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        project_user_obj = get_object_or_404(ProjectUser, pk=self.kwargs.get("project_user_pk"))

        project_user_update_form = ProjectUserUpdateForm(
            initial={"role": project_user_obj.role, "enable_notifications": project_user_obj.enable_notifications}
        )

        context = {}
        context["project_obj"] = project_obj
        context["project_user_update_form"] = project_user_update_form
        context["project_user_obj"] = project_user_obj

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        project_user_pk = self.kwargs.get("project_user_pk")

        if project_obj.status.name not in [
            "Active",
            "New",
        ]:
            messages.error(request, "You cannot update a user in an archived project.")
            return HttpResponseRedirect(reverse("project-user-detail", kwargs={"pk": project_user_pk}))

        if project_obj.projectuser_set.filter(id=project_user_pk).exists():
            project_user_obj = project_obj.projectuser_set.get(pk=project_user_pk)

            if project_user_obj.user == project_user_obj.project.pi:
                messages.error(request, "PI role and email notification option cannot be changed.")
                return HttpResponseRedirect(reverse("project-user-detail", kwargs={"pk": project_user_pk}))

            project_user_update_form = ProjectUserUpdateForm(
                request.POST,
                initial={
                    "role": project_user_obj.role.name,
                    "enable_notifications": project_user_obj.enable_notifications,
                },
            )

            if project_user_update_form.is_valid():
                form_data = project_user_update_form.cleaned_data
                project_user_obj.role = ProjectUserRoleChoice.objects.get(name=form_data.get("role"))

                if project_user_obj.role.name == "Manager":
                    project_user_obj.enable_notifications = True
                else:
                    project_user_obj.enable_notifications = form_data.get("enable_notifications")
                project_user_obj.save()

                messages.success(request, "User details updated.")
                return HttpResponseRedirect(
                    reverse(
                        "project-user-detail", kwargs={"pk": project_obj.pk, "project_user_pk": project_user_obj.pk}
                    )
                )
