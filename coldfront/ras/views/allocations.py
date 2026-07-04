# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string

from coldfront.ras import filtersets, flows, forms, tables
from coldfront.ras import object_actions as actions
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.ras.models import Allocation, Project
from coldfront.registry import register_model_view
from coldfront.views import generic
from coldfront.views.mixins import GetRelatedModelsMixin

try:
    ALLOCATION_WORKFLOW = import_string(settings.ALLOCATION_WORKFLOW)
except ImportError:
    raise ImproperlyConfigured("ALLOCATION_WORKFLOW was set but cannot be imported. Please check your config settings.")

#
# Allocations
#


@register_model_view(Allocation, "list", path="", detail=False)
class AllocationListView(generic.ObjectListView):
    queryset = Allocation.objects.all()
    filterset = filtersets.AllocationFilterSet
    filterset_form = forms.AllocationFilterSetForm
    table = tables.AllocationTable


@register_model_view(Allocation)
class AllocationView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = Allocation.objects.all()
    flow = flows.AllocationStatusFlow

    def get_extra_context(self, request, instance):
        # Get the outgoing transitions for the current status so we can display the appropriate buttons
        actions = AllocationStatusFlow.get_actions(instance.get_outgoing_transitions())
        transitions = self.get_permitted_actions(request.user, model=Allocation, actions=actions) if actions else None

        # Check if the resource provides a custom post-request form URL
        allocation_request_url = None
        if instance.resource_object:
            allocation_request_url = instance.resource_object.allocation_request_url(instance)

        return {
            "transitions": transitions,
            "related_models": self.get_related_models(request, instance),
            "allocation_request_url": allocation_request_url,
        }


@register_model_view(Allocation, "add", detail=False)
@register_model_view(Allocation, "edit")
class AllocationEditView(generic.ObjectEditView):
    queryset = Allocation.objects.all()
    form = forms.AllocationForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.owner = request.user

        return super().alter_object(obj, request, url_args, url_kwargs)


@register_model_view(Allocation, "delete")
class AllocationDeleteView(generic.ObjectDeleteView):
    queryset = Allocation.objects.all()


@register_model_view(Allocation, "bulk_import", path="import", detail=False)
class AllocationBulkImportView(generic.BulkImportView):
    queryset = Allocation.objects.all()
    model_form = forms.AllocationImportForm


@register_model_view(Allocation, "bulk_delete", path="delete", detail=False)
class AllocationBulkDeleteView(generic.BulkDeleteView):
    queryset = Allocation.objects.all()
    filterset = filtersets.AllocationFilterSet
    table = tables.AllocationTable


#
# Allocation status workflow
#


class BaseAllocationFlowView(generic.ObjectFlowView):
    queryset = Allocation.objects.all()
    form = forms.AllocationReviewForm
    flow = ALLOCATION_WORKFLOW


# Allocations are requested from a project
@register_model_view(Project, "allocationrequest", path="allocation-request")
class AllocationRequestView(BaseAllocationFlowView):
    template_name = "ras/project/allocation_request.html"
    form = forms.AllocationRequestForm
    action = actions.RequestObject

    def get_object(self, **kwargs):
        project = get_object_or_404(Project.objects.all(), **kwargs)
        return Allocation(project=project, tenant=project.tenant)

    def alter_object(self, obj, request, url_args, url_kwargs):
        # Check to ensure allocations requests are allowed
        flow = self.flow(obj)
        if not flow.can_request(request.user):
            raise PermissionDenied

        obj.owner = request.user
        return obj

    def get_return_url(self, request, obj=None):
        # Check if the resource provides a custom redirect for the
        # post-request form (e.g., to collect resource-specific data)
        if obj is not None and obj.pk and obj.resource_object:
            url = obj.resource_object.allocation_request_url(obj)
            if url:
                return url
        return super().get_return_url(request, obj)


@register_model_view(Allocation, "approve")
class AllocationApproveView(BaseAllocationFlowView):
    action = actions.ApproveObject


@register_model_view(Allocation, "deny")
class AllocationDenyView(BaseAllocationFlowView):
    action = actions.DenyObject


@register_model_view(Allocation, "revoke")
class AllocationRevokeView(BaseAllocationFlowView):
    action = actions.RevokeObject


@register_model_view(Allocation, "renew")
class AllocationRenewView(BaseAllocationFlowView):
    action = actions.RenewObject


@register_model_view(Allocation, "activate")
class AllocationActivateView(BaseAllocationFlowView):
    form = forms.AllocationActivateForm
    action = actions.ActivateObject
