# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render

from coldfront.core.allocation.models import Allocation, AllocationAttribute
from coldfront.core.utils.common import import_from_settings

SLURM_SUBMISSION_INFO = import_from_settings("SLURM_SUBMISSION_INFO", ["account"])
SLURM_DISPLAY_SHORT_OPTION_NAMES = import_from_settings("SLURM_DISPLAY_SHORT_OPTION_NAMES", False)
SLURM_SHORT_OPTION_NAMES = import_from_settings("SLURM_SHORT_OPTION_NAMES", {})


@login_required
def get_full_slurm_help(request):
    allocation_objs = (
        Allocation.objects.filter(
            status__name__in=[
                "Active",
                "Renewal Requested",
            ],
            allocationuser__user=request.user,
            allocationuser__status__name="Active",
            project__status__name="Active",
            allocationattribute__allocation_attribute_type__name__in=["slurm_account_name", "slurm_specs"],
        )
        .select_related("project")
        .prefetch_related(
            Prefetch(
                lookup="allocationattribute_set",
                queryset=AllocationAttribute.objects.filter(allocation_attribute_type__name="slurm_account_name"),
                to_attr="slurm_account_name",
            ),
            Prefetch(
                lookup="allocationattribute_set",
                queryset=AllocationAttribute.objects.filter(allocation_attribute_type__name="slurm_specs"),
                to_attr="slurm_specs",
            ),
        )
    )

    slurm_info = {}
    for allocation_obj in allocation_objs:
        if not slurm_info.get(allocation_obj.project_id):
            slurm_info[allocation_obj.project_id] = {"project_title": allocation_obj.project.title, "submit_info": {}}
        slurm_info[allocation_obj.project_id]["submit_info"].update(get_slurm_info_from_allocation(allocation_obj))

    return render(request, "slurm/full_slurm_help.html", {"slurm_info": slurm_info})


@login_required
def get_slurm_help(request):
    allocation_obj = (
        Allocation.objects.filter(pk=request.POST.get("allocation_pk"))
        .prefetch_related(
            Prefetch(
                lookup="allocationattribute_set",
                queryset=AllocationAttribute.objects.filter(allocation_attribute_type__name="slurm_account_name"),
                to_attr="slurm_account_name",
            ),
            Prefetch(
                lookup="allocationattribute_set",
                queryset=AllocationAttribute.objects.filter(allocation_attribute_type__name="slurm_specs"),
                to_attr="slurm_specs",
            ),
        )
        .first()
    )
    slurm_info = get_slurm_info_from_allocation(allocation_obj)
    return render(request, "slurm/slurm_help.html", {"slurm_info": slurm_info})


def get_slurm_info_from_allocation(allocation_obj):  # noqa: C901 # FIXME: method is too complex
    submit_options = {}
    resource_obj = allocation_obj.get_parent_resource
    resource_type = resource_obj.resource_type.name
    if resource_type == "Cluster Partition":
        cluster_obj = resource_obj.parent_resource
        if "clusters" in SLURM_SUBMISSION_INFO:
            submit_options["clusters"] = cluster_obj.resourceattribute_set.get(
                resource_attribute_type__name="slurm_cluster"
            ).value
        if "partition" in SLURM_SUBMISSION_INFO:
            submit_options["partition"] = resource_obj.name.lower()
    elif resource_type != "Cluster":
        return {}

    slurm_account = allocation_obj.slurm_account_name
    if slurm_account:
        if "account" in SLURM_SUBMISSION_INFO:
            submit_options["account"] = slurm_account[0].value

    slurm_specs = resource_obj.resourceattribute_set.filter(resource_attribute_type__name="slurm_specs")
    submit_options = get_slurm_info_from_slurm_specs(slurm_specs, submit_options)
    slurm_specs = allocation_obj.slurm_specs
    submit_options = get_slurm_info_from_slurm_specs(slurm_specs, submit_options)

    if SLURM_DISPLAY_SHORT_OPTION_NAMES:
        submit_short_options = {}
        for option, value in submit_options.items():
            short_option = SLURM_SHORT_OPTION_NAMES.get(option)
            if short_option:
                submit_short_options["-" + short_option] = value
            else:
                submit_short_options["--" + option] = value

        slurm_info = submit_short_options
    else:
        submit_long_options = {}
        for option, value in submit_options.items():
            submit_long_options["--" + option] = value

        slurm_info = submit_long_options

    return {resource_obj.name: slurm_info}


def get_slurm_info_from_slurm_specs(slurm_specs, submit_options):
    if slurm_specs:
        specs = slurm_specs[0].value.replace("+", "").split(":")
        for spec in specs:
            spec_split = spec.split("=")
            # Expanded attributes should be skipped
            if len(spec_split) > 2:
                continue
            option, value = spec_split
            option = option.lower()
            if option in SLURM_SUBMISSION_INFO:
                submit_options[option] = value

    return submit_options
