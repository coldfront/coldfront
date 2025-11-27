# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from coldfront.core.project.forms import ProjectCreationForm
from coldfront.core.project.models import (
    Project,
    ProjectStatusChoice,
    ProjectUserRoleChoice,
)
from coldfront.core.project.signals import (
    project_new,
    project_update,
)
from coldfront.core.project.utils import (
    add_institution,
    add_project_code_if_missing,
    add_user_to_project,
    project_is_archived,
    user_is_pi_or_manager,
)


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    template_name_suffix = "_create_form"
    form_class = ProjectCreationForm

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.userprofile.is_pi:
            return True

    def form_valid(self, form):
        project_obj = form.save(commit=False)
        form.instance.pi = self.request.user
        form.instance.status = ProjectStatusChoice.objects.get(name="New")
        project_obj.save()
        self.object = project_obj

        # ensure project code is set if missing and feature is enabled
        add_project_code_if_missing(project_obj)

        # set automated institution if enabled
        add_institution(project_obj)

        # add the creating user as Manager
        add_user_to_project(
            project_obj,
            self.request.user,
            ProjectUserRoleChoice.objects.get(name="Manager"),
            send_signals=False,
        )

        # project signals
        project_new.send(sender=self.__class__, project_obj=project_obj)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name_suffix = "_update_form"
    fields = [
        "title",
        "description",
        "field_of_science",
    ]
    success_message = "Project updated."

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return user_is_pi_or_manager(self.request.user, project_obj)

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        # ensure project code is set if missing and feature is enabled
        add_project_code_if_missing(project_obj)

        if project_is_archived(project_obj):
            messages.error(request, "You cannot update an archived project.")
            return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # project signals
        project_update.send(sender=self.__class__, project_obj=self.object)
        return reverse("project-detail", kwargs={"pk": self.object.pk})
