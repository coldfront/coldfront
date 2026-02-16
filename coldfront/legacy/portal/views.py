# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
from collections import Counter

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import FloatField, Q, Sum
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from coldfront.legacy.allocation.models import Allocation, AllocationUser
from coldfront.legacy.grant.models import Grant
from coldfront.legacy.project.models import Project
from coldfront.legacy.research_output.models import ResearchOutput
from coldfront.legacy.utils.common import import_from_settings

ALLOCATION_EULA_ENABLE = import_from_settings("ALLOCATION_EULA_ENABLE", False)


def home(request):
    context = {}
    if request.user.is_authenticated:
        template_name = "portal/authorized_home.html"
        project_list = (
            Project.objects.select_related("status")
            .filter(
                (
                    Q(pi=request.user)
                    & Q(
                        status__name__in=[
                            "New",
                            "Active",
                        ]
                    )
                )
                | (
                    Q(
                        status__name__in=[
                            "New",
                            "Active",
                        ]
                    )
                    & Q(projectuser__user=request.user)
                    & Q(
                        projectuser__status__name__in=[
                            "Active",
                        ]
                    )
                )
            )
            .distinct()
            .order_by("-created")[:5]
        )

        allocation_list = (
            Allocation.objects.select_related("status", "project")
            .filter(
                Q(
                    status__name__in=[
                        "Active",
                        "New",
                        "Renewal Requested",
                    ]
                )
                & Q(project__status__name__in=["Active", "New"])
                & Q(project__projectuser__user=request.user)
                & Q(
                    project__projectuser__status__name__in=[
                        "Active",
                    ]
                )
                & Q(allocationuser__user=request.user)
                & Q(allocationuser__status__name__in=["Active", "PendingEULA"])
            )
            .distinct()
            .order_by("-created")[:5]
        )

        if ALLOCATION_EULA_ENABLE:
            user_status = []
            for allocation in allocation_list:
                if allocation.allocationuser_set.filter(user=request.user).exists():
                    user_status.append(allocation.allocationuser_set.get(user=request.user).status.name)
            context["user_status"] = user_status

        context["project_list"] = project_list
        context["allocation_list"] = allocation_list

        try:
            context["ondemand_url"] = settings.ONDEMAND_URL
        except AttributeError:
            pass
    else:
        template_name = "portal/nonauthorized_home.html"

    context["EXTRA_APPS"] = settings.INSTALLED_APPS

    if "coldfront.legacy.plugins.system_monitor" in settings.INSTALLED_APPS:
        from coldfront.legacy.plugins.system_monitor.utils import get_system_monitor_context

        context.update(get_system_monitor_context())

    return render(request, template_name, context)


def center_summary(request):
    context = {}
    context["research_outputs_count"] = ResearchOutput.objects.all().distinct().count()

    sum_agg = Sum(Cast("total_amount_awarded", FloatField()), default=0)
    context["grant_total"] = intcomma(
        int(Grant.objects.aggregate(total_amount_awarded__sum=sum_agg)["total_amount_awarded__sum"])
    )
    context["grant_total_pi_only"] = intcomma(
        int(Grant.objects.filter(role="PI").aggregate(total_amount_awarded__sum=sum_agg)["total_amount_awarded__sum"])
    )
    context["grant_total_copi_only"] = intcomma(
        int(Grant.objects.filter(role="CoPI").aggregate(total_amount_awarded__sum=sum_agg)["total_amount_awarded__sum"])
    )
    context["grant_total_sp_only"] = intcomma(
        int(Grant.objects.filter(role="SP").aggregate(total_amount_awarded__sum=sum_agg)["total_amount_awarded__sum"])
    )
    return render(request, "portal/center_summary.html", context)


@cache_page(60 * 15)
def allocation_by_fos(request):
    allocations_by_fos = Counter(
        list(
            Allocation.objects.filter(status__name="Active").values_list(
                "project__field_of_science__description", flat=True
            )
        )
    )

    user_allocations = AllocationUser.objects.filter(status__name="Active", allocation__status__name="Active")

    active_users_by_fos = Counter(
        list(user_allocations.values_list("allocation__project__field_of_science__description", flat=True))
    )
    total_allocations_users = user_allocations.values("user").distinct().count()

    active_pi_count = (
        Project.objects.filter(status__name__in=["Active", "New"])
        .values_list("pi__username", flat=True)
        .distinct()
        .count()
    )
    context = {}
    context["allocations_by_fos"] = dict(allocations_by_fos)
    context["active_users_by_fos"] = dict(active_users_by_fos)
    context["total_allocations_users"] = total_allocations_users
    context["active_pi_count"] = active_pi_count
    return render(request, "portal/allocation_by_fos.html", context)


@cache_page(60 * 15)
def allocation_summary(request):
    allocation_resources = []
    for allocation in Allocation.objects.filter(status__name="Active"):
        parent_resource = allocation.get_parent_resource
        allocation_resources.append(
            parent_resource.parent_resource if parent_resource.parent_resource else parent_resource
        )

    allocations_count_by_resource = dict(Counter(allocation_resources))

    context = {}
    context["allocations_count_by_resource"] = allocations_count_by_resource

    return render(request, "portal/allocation_summary.html", context)


def allocation_by_status(request):
    data = [
        {"name": "Active", "total": Allocation.objects.filter(status__name="Active").count()},
        {"name": "New", "total": Allocation.objects.filter(status__name="New").count()},
        {"name": "Renewal Requested", "total": Allocation.objects.filter(status__name="Renewal Requested").count()},
    ]

    now = datetime.datetime.now()
    start_time = datetime.date(now.year - 1, 1, 1)
    data.append(
        {
            "name": "Expired",
            "total": Allocation.objects.filter(status__name="Expired", end_date__gte=start_time).count(),
        }
    )

    return JsonResponse({"data": data})


def resource_by_type(request):
    allocation_resources = []
    for allocation in Allocation.objects.filter(status__name="Active"):
        parent_resource = allocation.get_parent_resource
        allocation_resources.append(
            parent_resource.parent_resource if parent_resource.parent_resource else parent_resource
        )

    allocation_count_by_resource_type = dict(Counter([ele.resource_type.name for ele in allocation_resources]))

    data = []
    for rtype in ["Cluster", "Cloud", "Server", "Storage"]:
        data.append({"name": rtype, "total": allocation_count_by_resource_type.get(rtype, 0)})

    return JsonResponse({"data": data})
