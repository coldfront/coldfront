# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from coldfront.core.allocation.models import AllocationStatusChoice
from coldfront.core.project.models import (
    Project,
    ProjectStatusChoice,
)
from coldfront.core.project.signals import project_archive
from coldfront.core.project.utils import user_is_pi_or_manager

logger = logging.getLogger(__name__)


class ProjectArchiveProjectView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_archive.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return user_is_pi_or_manager(self.request.user, project_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["project"] = get_object_or_404(Project, pk=pk)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)
        project.status = ProjectStatusChoice.objects.get(name="Archived")
        project.save()

        # project_archive signal
        project_archive.send(sender=self.__class__, project_obj=project)

        # Archive all active allocations linked to this project
        allocation_status_expired = AllocationStatusChoice.objects.get(name="Expired")
        end_date = datetime.datetime.now()

        for allocation in project.allocation_set.filter(status__name="Active"):
            allocation.status = allocation_status_expired
            allocation.end_date = end_date
            allocation.save()
        return redirect(reverse("project-detail", kwargs={"pk": project.pk}))
