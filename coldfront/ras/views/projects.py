# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from coldfront.ras import filtersets, forms, tables
from coldfront.ras.models import Allocation, Project
from coldfront.registry import register_model_view
from coldfront.views import ViewTab, generic
from coldfront.views.mixins import GetRelatedModelsMixin
from coldfront.views.object_actions import BulkExport

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
