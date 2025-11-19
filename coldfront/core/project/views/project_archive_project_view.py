# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView

from coldfront.core.allocation.models import AllocationStatusChoice
from coldfront.core.project.models import Project, ProjectStatusChoice
from coldfront.core.project.signals import project_archive


class ProjectArchiveProjectView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_archive.html"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)

        context["project"] = project

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)
        project_status_archive = ProjectStatusChoice.objects.get(name="Archived")
        allocation_status_expired = AllocationStatusChoice.objects.get(name="Expired")
        end_date = datetime.datetime.now()
        project.status = project_status_archive
        project.save()

        # project signals
        project_archive.send(sender=self.__class__, project_obj=project)

        for allocation in project.allocation_set.filter(status__name="Active"):
            allocation.status = allocation_status_expired
            allocation.end_date = end_date
            allocation.save()
        return redirect(project)
