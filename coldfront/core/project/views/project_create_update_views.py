# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView

from coldfront.core.project.forms import ProjectCreationForm
from coldfront.core.project.models import (
    Project,
    ProjectStatusChoice,
    ProjectUser,
    ProjectUserRoleChoice,
    ProjectUserStatusChoice,
)
from coldfront.core.project.signals import project_new, project_update
from coldfront.core.project.utils import determine_automated_institution_choice, generate_project_code
from coldfront.core.utils.common import import_from_settings

PROJECT_CODE = import_from_settings("PROJECT_CODE", False)
PROJECT_CODE_PADDING = import_from_settings("PROJECT_CODE_PADDING", False)
PROJECT_UPDATE_FIELDS = import_from_settings(
    "PROJECT_UPDATE_FIELDS",
    [
        "title",
        "description",
        "field_of_science",
    ],
)
PROJECT_INSTITUTION_EMAIL_MAP = import_from_settings("PROJECT_INSTITUTION_EMAIL_MAP", False)


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

        ProjectUser.objects.create(
            user=self.request.user,
            project=project_obj,
            role=ProjectUserRoleChoice.objects.get(name="Manager"),
            status=ProjectUserStatusChoice.objects.get(name="Active"),
        )

        if PROJECT_CODE:
            """
            Set the ProjectCode object, if PROJECT_CODE is defined. 
            If PROJECT_CODE_PADDING is defined, the set amount of padding will be added to PROJECT_CODE.
            """
            project_obj.project_code = generate_project_code(PROJECT_CODE, project_obj.pk, PROJECT_CODE_PADDING or 0)
            project_obj.save(update_fields=["project_code"])

        if PROJECT_INSTITUTION_EMAIL_MAP:
            determine_automated_institution_choice(project_obj, PROJECT_INSTITUTION_EMAIL_MAP)

        # project signals
        project_new.send(sender=self.__class__, project_obj=project_obj)

        return super().form_valid(form)


class ProjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name_suffix = "_update_form"
    fields = PROJECT_UPDATE_FIELDS
    success_message = "Project updated."

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        project_obj = self.get_object()

        if project_obj.pi == self.request.user:
            return True

        if project_obj.projectuser_set.filter(
            user=self.request.user, role__name="Manager", status__name="Active"
        ).exists():
            return True

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if PROJECT_CODE and project_obj.project_code == "":
            """
            Updates project code if no value was set, providing the feature is activated. 
            """
            project_obj.project_code = generate_project_code(PROJECT_CODE, project_obj.pk, PROJECT_CODE_PADDING or 0)
            project_obj.save(update_fields=["project_code"])

        if project_obj.status.name not in [
            "Active",
            "New",
        ]:
            messages.error(request, "You cannot update an archived project.")
            return redirect(project_obj.pk)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # project signals
        project_update.send(sender=self.__class__, project_obj=self.object)
        return super().get_success_url()
