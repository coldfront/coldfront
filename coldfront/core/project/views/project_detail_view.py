# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from coldfront.core.allocation.models import Allocation
from coldfront.core.grant.models import Grant
from coldfront.core.project.models import Project
from coldfront.core.project.utils import (
    get_project_attributes,
    project_attribute_with_usage_to_gauge,
    user_can_view_project,
    user_is_pi_or_manager,
)
from coldfront.core.publication.models import Publication
from coldfront.core.research_output.models import ResearchOutput

logger = logging.getLogger(__name__)


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = "project/project_detail.html"
    context_object_name = "project"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = self.get_object()
        if user_can_view_project(self.request.user, project_obj):
            return True

        messages.error(self.request, "You do not have permission to view the previous page.")
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Can the user update the project?
        is_allowed_to_update = user_is_pi_or_manager(self.request.user, self.object)
        context["is_allowed_to_update_project"] = is_allowed_to_update

        # is this needed? pk is in self.object
        pk = self.kwargs.get("pk")
        project_obj = get_object_or_404(Project, pk=pk)

        # only show private attributes to superusers
        attributes = get_project_attributes(project_obj, show_private=self.request.user.is_superuser)
        attributes_with_usage = [a for a in attributes if hasattr(a, "projectattributeusage")]

        gauge_data = []
        for attribute in attributes_with_usage:
            attr_data = project_attribute_with_usage_to_gauge(attribute)
            if attr_data is not None:
                gauge_data.append(attr_data)
            else:
                # Remove attributes with usage that cannot be represented as gauges
                attributes_with_usage.remove(attribute)

        # Only show 'Active Users'
        project_users = self.object.projectuser_set.filter(status__name="Active").order_by("user__username")

        context["mailto"] = "mailto:" + ",".join([user.user.email for user in project_users])

        allocations = get_project_allocations(self.object, self.request.user)

        user_status = []
        for allocation in allocations:
            if allocation.allocationuser_set.filter(user=self.request.user).exists():
                user_status.append(allocation.allocationuser_set.get(user=self.request.user).status.name)

        context["publications"] = Publication.objects.filter(project=self.object, status="Active").order_by("-year")
        context["research_outputs"] = ResearchOutput.objects.filter(project=self.object).order_by("-created")
        context["grants"] = Grant.objects.filter(
            project=self.object, status__name__in=["Active", "Pending", "Archived"]
        )
        context["allocations"] = allocations
        context["user_allocation_status"] = user_status
        context["attributes"] = attributes
        context["gauge_data"] = gauge_data
        context["attributes_with_usage"] = attributes_with_usage
        context["project_users"] = project_users

        if hasattr(settings, "ONDEMAND_URL"):
            context["ondemand_url"] = settings.ONDEMAND_URL

        return context


def get_project_allocations(project_obj, user_obj):
    """Get active allocations for a project"""
    if (
        user_obj.is_superuser
        or user_obj.has_perm("allocation.can_view_all_allocations")
        or project_obj.status.name not in ["Active", "New"]
    ):
        # show all project allocations
        return Allocation.objects.prefetch_related("resources").filter(project=project_obj).order_by("-end_date")
    else:
        # only show allocations the user is part of
        return (
            Allocation.objects.filter(
                Q(project=project_obj)
                & Q(project__projectuser__user=user_obj)
                & Q(
                    project__projectuser__status__name__in=[
                        "Active",
                    ]
                )
                & Q(allocationuser__user=user_obj)
                & Q(allocationuser__status__name__in=["Active", "PendingEULA"])
            )
            .distinct()
            .order_by("-end_date")
        )
