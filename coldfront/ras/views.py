# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.utils.translation import gettext_lazy as _

from coldfront.registry import register_model_view
from coldfront.utils.query import count_related
from coldfront.views import ViewTab, generic
from coldfront.views.mixins import GetRelatedModelsMixin
from coldfront.views.object_actions import BulkExport

from . import filtersets, forms, tables
from .models import Allocation, AllocationType, Project, Resource, ResourceType

#
# Resource types
#


@register_model_view(ResourceType, "list", path="", detail=False)
class ResourceTypeListView(generic.ObjectListView):
    queryset = ResourceType.objects.annotate(
        resource_count=count_related(Resource, "resource_type"),
    )
    filterset = filtersets.ResourceTypeFilterSet
    filterset_form = forms.ResourceTypeFilterSetForm
    table = tables.ResourceTypeTable


@register_model_view(ResourceType)
class ResourceTypeView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = ResourceType.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(request, instance),
        }


@register_model_view(ResourceType, "add", detail=False)
@register_model_view(ResourceType, "edit")
class ResourceTypeEditView(generic.ObjectEditView):
    queryset = ResourceType.objects.all()
    form = forms.ResourceTypeForm


@register_model_view(ResourceType, "delete")
class ResourceTypeDeleteView(generic.ObjectDeleteView):
    queryset = ResourceType.objects.all()


#
# Resources
#


@register_model_view(Resource, "list", path="", detail=False)
class ResourceListView(generic.ObjectListView):
    queryset = Resource.objects.all()
    filterset = filtersets.ResourceFilterSet
    filterset_form = forms.ResourceFilterSetForm
    table = tables.ResourceTable


@register_model_view(Resource)
class ResourceView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = Resource.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(request, instance),
        }


@register_model_view(Resource, "add", detail=False)
@register_model_view(Resource, "edit")
class ResourceEditView(generic.ObjectEditView):
    queryset = Resource.objects.all()
    form = forms.ResourceForm


@register_model_view(Resource, "delete")
class ResourceDeleteView(generic.ObjectDeleteView):
    queryset = Resource.objects.all()


#
# Projects
#


@register_model_view(Project, "list", path="", detail=False)
class ProjectListView(generic.ObjectListView):
    queryset = Project.objects.all()
    filterset = filtersets.ProjectFilterSet
    filterset_form = forms.ProjectFilterSetForm
    table = tables.ProjectTable


@register_model_view(Project)
class ProjectView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = Project.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(request, instance),
        }


@register_model_view(Project, "add", detail=False)
@register_model_view(Project, "edit")
class ProjectEditView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.owner = request.user

        return super().alter_object(obj, request, url_args, url_kwargs)


@register_model_view(Project, "delete")
class ProjectDeleteView(generic.ObjectDeleteView):
    queryset = Project.objects.all()


@register_model_view(Project, "allocations")
class ProjectAllocationsView(generic.ObjectChildrenView):
    actions = (BulkExport,)
    queryset = Project.objects.all()
    child_model = Allocation
    table = tables.AllocationTable
    filterset = filtersets.AllocationFilterSet
    filterset_form = forms.AllocationFilterSetForm
    template_name = "ras/project/allocations.html"
    tab = ViewTab(
        label=_("Allocations"), badge=lambda obj: obj.allocations.count(), permission="ras.view_allocation", weight=510
    )

    def get_children(self, request, parent):
        return parent.allocations.restrict(request.user, "view")


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
