# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from coldfront.ras import filtersets, flows, forms, tables
from coldfront.ras import object_actions as actions
from coldfront.ras.flows import AllocationStatusFlow
from coldfront.ras.models import Allocation, AllocationUser, Project, Resource
from coldfront.registry import register_model_view
from coldfront.views import ViewTab, generic
from coldfront.views.mixins import GetRelatedModelsMixin
from coldfront.views.object_actions import BulkDelete, BulkExport

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
        return {
            "transitions": transitions,
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


@register_model_view(Allocation, "users")
class AllocationUserTabView(generic.ObjectChildrenView):
    actions = (BulkExport, BulkDelete)
    queryset = Allocation.objects.all()
    child_model = AllocationUser
    table = tables.AllocationUserTable
    filterset = filtersets.AllocationUserFilterSet
    template_name = "ras/allocation/users.html"
    tab = ViewTab(
        label=_("Users"),
        badge=lambda obj: obj.users.count(),
        permission="ras.view_allocation",
        weight=100,
    )

    def get_children(self, request, parent):
        return parent.users.restrict(request.user, "view")

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        # TODO: hide this column by default? add created?
        table.columns.hide("allocation")
        table.columns.hide("project")
        table.columns.show("created")
        return table


@register_model_view(Allocation, "resources")
class AllocationResourceTabView(generic.ObjectChildrenView):
    actions = (BulkExport,)
    queryset = Allocation.objects.all()
    child_model = Resource
    table = tables.ResourceTable
    filterset = filtersets.ResourceFilterSet
    template_name = "ras/allocation/resources.html"
    tab = ViewTab(
        label=_("Resources"),
        badge=lambda obj: obj.resource.get_descendants(include_self=True).count(),
        permission="ras.view_allocation",
        weight=110,
    )

    def get_children(self, request, parent):
        return parent.resource.get_descendants(include_self=True)

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        table.columns.hide("allocation_count")
        return table


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

    def post_save(self, obj, form, request):
        # Create the allocation users
        for user in form.cleaned_data["users"]:
            AllocationUser.objects.create(user=user, allocation=obj)


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


#
# Allocation Users
#


@register_model_view(AllocationUser, "list", path="", detail=False)
class AllocationUserListView(generic.ObjectListView):
    queryset = AllocationUser.objects.all()
    filterset = filtersets.AllocationUserFilterSet
    filterset_form = forms.AllocationUserFilterSetForm
    table = tables.AllocationUserTable


@register_model_view(AllocationUser)
class AllocationUserView(generic.ObjectView):
    queryset = AllocationUser.objects.all()


@register_model_view(AllocationUser, "add", detail=False)
@register_model_view(AllocationUser, "edit")
class AllocationUserEditView(generic.ObjectEditView):
    queryset = AllocationUser.objects.all()
    form = forms.AllocationUserForm


@register_model_view(AllocationUser, "delete")
class AllocationUserDeleteView(generic.ObjectDeleteView):
    queryset = AllocationUser.objects.all()


@register_model_view(AllocationUser, "bulk_import", path="import", detail=False)
class AllocationUserBulkImportView(generic.BulkImportView):
    queryset = AllocationUser.objects.all()
    model_form = forms.AllocationUserImportForm


@register_model_view(AllocationUser, "bulk_delete", path="delete", detail=False)
class AllocationUserBulkDeleteView(generic.BulkDeleteView):
    queryset = AllocationUser.objects.all()
    filterset = filtersets.AllocationUserFilterSet
    table = tables.AllocationUserTable
