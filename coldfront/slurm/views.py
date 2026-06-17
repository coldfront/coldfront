# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0


from coldfront.registry import register_model_view
from coldfront.slurm import filtersets, forms, tables
from coldfront.slurm.models import SlurmCluster, SlurmPartition
from coldfront.utils.query import count_related
from coldfront.views import generic
from coldfront.views.mixins import GetRelatedModelsMixin

#
# Slurm clusters
#


@register_model_view(SlurmCluster, "list", path="", detail=False)
class SlurmClusterListView(generic.ObjectListView):
    queryset = SlurmCluster.objects.annotate(
        partition_count=count_related(SlurmPartition, "cluster"),
    )
    filterset = filtersets.SlurmClusterFilterSet
    filterset_form = forms.SlurmClusterFilterSetForm
    table = tables.SlurmClusterTable


@register_model_view(SlurmCluster)
class SlurmClusterView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = SlurmCluster.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(request, instance),
        }


@register_model_view(SlurmCluster, "add", detail=False)
@register_model_view(SlurmCluster, "edit")
class SlurmClusterEditView(generic.ObjectEditView):
    queryset = SlurmCluster.objects.all()
    form = forms.SlurmClusterForm


@register_model_view(SlurmCluster, "delete")
class SlurmClusterDeleteView(generic.ObjectDeleteView):
    queryset = SlurmCluster.objects.all()


@register_model_view(SlurmCluster, "bulk_import", path="import", detail=False)
class SlurmClusterBulkImportView(generic.BulkImportView):
    queryset = SlurmCluster.objects.all()
    model_form = forms.SlurmClusterImportForm


@register_model_view(SlurmCluster, "bulk_delete", path="delete", detail=False)
class SlurmClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = SlurmCluster.objects.all()
    filterset = filtersets.SlurmClusterFilterSet
    table = tables.SlurmClusterTable


#
# Slurm partitions
#


@register_model_view(SlurmPartition, "list", path="", detail=False)
class SlurmPartitionListView(generic.ObjectListView):
    queryset = SlurmPartition.objects.all()
    filterset = filtersets.SlurmPartitionFilterSet
    filterset_form = forms.SlurmPartitionFilterSetForm
    table = tables.SlurmPartitionTable


@register_model_view(SlurmPartition)
class SlurmPartitionView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = SlurmPartition.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(request, instance),
        }


@register_model_view(SlurmPartition, "add", detail=False)
@register_model_view(SlurmPartition, "edit")
class SlurmPartitionEditView(generic.ObjectEditView):
    queryset = SlurmPartition.objects.all()
    form = forms.SlurmPartitionForm


@register_model_view(SlurmPartition, "delete")
class SlurmPartitionDeleteView(generic.ObjectDeleteView):
    queryset = SlurmPartition.objects.all()


@register_model_view(SlurmPartition, "bulk_import", path="import", detail=False)
class SlurmPartitionBulkImportView(generic.BulkImportView):
    queryset = SlurmPartition.objects.all()
    model_form = forms.SlurmPartitionImportForm


@register_model_view(SlurmPartition, "bulk_delete", path="delete", detail=False)
class SlurmPartitionBulkDeleteView(generic.BulkDeleteView):
    queryset = SlurmPartition.objects.all()
    filterset = filtersets.SlurmPartitionFilterSet
    table = tables.SlurmPartitionTable
