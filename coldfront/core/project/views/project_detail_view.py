# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import DetailView

from coldfront.core.allocation.models import Allocation
from coldfront.core.allocation.utils import generate_guauge_data_from_usage
from coldfront.core.grant.models import Grant
from coldfront.core.project.models import Project
from coldfront.core.publication.models import Publication
from coldfront.core.research_output.models import ResearchOutput

logger = logging.getLogger(__name__)


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = "project/project_detail.html"
    context_object_name = "project"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("project.can_view_all_projects"):
            return True

        project_obj = self.get_object()

        if project_obj.projectuser_set.filter(user=self.request.user, status__name="Active").exists():
            return True

        messages.error(self.request, "You do not have permission to view the previous page.")
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Can the user update the project?
        project_obj = self.get_object(Project.objects.select_related("status"))
        project_user = project_obj.projectuser_set.select_related("role").filter(user=self.request.user)
        if self.request.user.is_superuser:
            context["is_allowed_to_update_project"] = True
        elif project_user:
            project_user = project_user.first()
            if project_user.role.name == "Manager":
                context["is_allowed_to_update_project"] = True
            else:
                context["is_allowed_to_update_project"] = False
        else:
            context["is_allowed_to_update_project"] = False

        attributes_query = project_obj.projectattribute_set.select_related("proj_attr_type", "projectattributeusage")
        if self.request.user.is_superuser:
            attributes_with_usage = [
                attribute
                for attribute in attributes_query.all().order_by("proj_attr_type__name")
                if hasattr(attribute, "projectattributeusage")
            ]

            attributes = [attribute for attribute in attributes_query.all().order_by("proj_attr_type__name")]

        else:
            attributes_with_usage = [
                attribute
                for attribute in attributes_query.filter(proj_attr_type__is_private=False)
                if hasattr(attribute, "projectattributeusage")
            ]

            attributes = [attribute for attribute in attributes_query.filter(proj_attr_type__is_private=False)]

        guage_data = []
        invalid_attributes = []
        for attribute in attributes_with_usage:
            try:
                guage_data.append(
                    generate_guauge_data_from_usage(
                        attribute.proj_attr_type.name,
                        float(attribute.value),
                        float(attribute.projectattributeusage.value),
                    )
                )
            except ValueError:
                logger.error(
                    "Allocation attribute '%s' is not an int but has a usage", attribute.allocation_attribute_type.name
                )
                invalid_attributes.append(attribute)

        for a in invalid_attributes:
            attributes_with_usage.remove(a)

        # Only show 'Active Users'
        project_users = (
            project_obj.projectuser_set.select_related("user", "role", "status")
            .filter(status__name="Active")
            .order_by("user__username")
        )

        context["mailto"] = "mailto:" + ",".join([user.user.email for user in project_users])

        allocations = Allocation.objects.select_related("status").prefetch_related("resources")
        if self.request.user.is_superuser or self.request.user.has_perm("allocation.can_view_all_allocations"):
            allocations = allocations.filter(project=project_obj).order_by("-end_date")
        else:
            if project_obj.status.name in [
                "Active",
                "New",
            ]:
                allocations = (
                    allocations.filter(
                        Q(project=project_obj)
                        & Q(project__projectuser__user=self.request.user)
                        & Q(
                            project__projectuser__status__name__in=[
                                "Active",
                            ]
                        )
                        & Q(allocationuser__user=self.request.user)
                        & Q(allocationuser__status__name__in=["Active", "PendingEULA"])
                    )
                    .distinct()
                    .order_by("-end_date")
                )
            else:
                allocations = allocations.filter(project=project_obj)

        user_status = []
        for allocation in allocations:
            allocation_user = allocation.allocationuser_set.select_related("status").filter(user=self.request.user)
            if allocation_user:
                user_status.append(allocation_user.first().status.name)

        note_set = project_obj.projectusermessage_set
        notes = note_set.all() if self.request.user.is_superuser else note_set.filter(is_private=False)
        context["notes"] = notes
        context["publications"] = (
            Publication.objects.select_related("source").filter(project=project_obj, status="Active").order_by("-year")
        )
        context["research_outputs"] = ResearchOutput.objects.filter(project=project_obj).order_by("-created")
        context["grants"] = Grant.objects.select_related("status").filter(
            project=project_obj, status__name__in=["Active", "Pending", "Archived"]
        )
        context["allocations"] = allocations
        context["user_allocation_status"] = user_status
        context["attributes"] = attributes
        context["guage_data"] = guage_data
        context["attributes_with_usage"] = attributes_with_usage
        context["project_users"] = project_users

        try:
            context["ondemand_url"] = settings.ONDEMAND_URL
        except AttributeError:
            pass

        return context
