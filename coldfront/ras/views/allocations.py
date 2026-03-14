# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0


from coldfront.ras import filtersets, forms, tables
from coldfront.ras.models import Allocation, AllocationType
from coldfront.registry import register_model_view
from coldfront.utils.query import count_related
from coldfront.views import generic
from coldfront.views.mixins import GetRelatedModelsMixin

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
