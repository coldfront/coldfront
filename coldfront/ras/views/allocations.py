# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from coldfront.ras import filtersets, forms, tables
from coldfront.ras.models import Allocation, AllocationType, AllocationUser, Resource
from coldfront.registry import register_model_view
from coldfront.utils.query import count_related
from coldfront.views import ViewTab, generic
from coldfront.views.mixins import GetRelatedModelsMixin
from coldfront.views.object_actions import BulkDelete, BulkExport

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
    queryset = Allocation.objects.prefetch_related("resources__resource_type")


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
    tab = ViewTab(label=_("Users"), badge=lambda obj: obj.users.count(), permission="ras.view_allocation", weight=100)

    def get_children(self, request, parent):
        return parent.users.restrict(request.user, "view")

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        # TODO: hide this column by default? add created?
        table.columns.hide("allocation")
        table.columns.show("created")
        return table


@register_model_view(Allocation, "resources")
class AllocationResourceTabView(generic.ObjectChildrenView):
    actions = (BulkExport, BulkDelete)
    queryset = Allocation.objects.all()
    child_model = Resource
    table = tables.ResourceTable
    filterset = filtersets.ResourceFilterSet
    template_name = "ras/allocation/resources.html"
    tab = ViewTab(
        label=_("Resources"), badge=lambda obj: obj.resources.count(), permission="ras.view_allocation", weight=110
    )

    def get_children(self, request, parent):
        return parent.resources.restrict(request.user, "view")

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        table.columns.hide("allocation_count")
        return table


#
# Allocation types
#


@register_model_view(AllocationType, "list", path="", detail=False)
class AllocationTypeListView(generic.ObjectListView):
    queryset = AllocationType.objects.annotate(
        allocation_count=count_related(Allocation, "allocation_type"),
    )
    filterset = filtersets.AllocationTypeFilterSet
    filterset_form = forms.AllocationTypeFilterSetForm
    table = tables.AllocationTypeTable


@register_model_view(AllocationType)
class AllocationTypeView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = AllocationType.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(request, instance),
        }


@register_model_view(AllocationType, "add", detail=False)
@register_model_view(AllocationType, "edit")
class AllocationTypeEditView(generic.ObjectEditView):
    queryset = AllocationType.objects.all()
    form = forms.AllocationTypeForm


@register_model_view(AllocationType, "delete")
class AllocationTypeDeleteView(generic.ObjectDeleteView):
    queryset = AllocationType.objects.all()


@register_model_view(AllocationType, "bulk_import", path="import", detail=False)
class AllocationTypeBulkImportView(generic.BulkImportView):
    queryset = AllocationType.objects.all()
    model_form = forms.AllocationTypeImportForm


@register_model_view(AllocationType, "bulk_delete", path="delete", detail=False)
class AllocationTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = AllocationType.objects.all()
    filterset = filtersets.AllocationTypeFilterSet
    table = tables.AllocationTypeTable


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
