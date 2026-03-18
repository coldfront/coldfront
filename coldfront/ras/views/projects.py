# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from coldfront.ras import filtersets, forms, tables
from coldfront.ras.models import Allocation, Project, ProjectUser
from coldfront.registry import register_model_view
from coldfront.utils.query import count_related
from coldfront.views import ViewTab, generic
from coldfront.views.mixins import GetRelatedModelsMixin
from coldfront.views.object_actions import BulkDelete, BulkExport

#
# Projects
#


@register_model_view(Project, "list", path="", detail=False)
class ProjectListView(generic.ObjectListView):
    queryset = Project.objects.annotate(
        user_count=count_related(ProjectUser, "project"),
        allocation_count=count_related(Allocation, "project"),
    )
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


@register_model_view(Project, "bulk_import", path="import", detail=False)
class ProjectBulkImportView(generic.BulkImportView):
    queryset = Project.objects.all()
    model_form = forms.ProjectImportForm


@register_model_view(Project, "bulk_delete", path="delete", detail=False)
class ProjectBulkDeleteView(generic.BulkDeleteView):
    queryset = Project.objects.all()
    filterset = filtersets.ProjectFilterSet
    table = tables.ProjectTable


@register_model_view(Project, "users")
class ProjectUserTabView(generic.ObjectChildrenView):
    actions = (BulkExport, BulkDelete)
    queryset = Project.objects.all()
    child_model = ProjectUser
    table = tables.ProjectUserTable
    filterset = filtersets.ProjectUserFilterSet
    filterset_form = forms.ProjectUserFilterSetForm
    template_name = "ras/project/users.html"
    tab = ViewTab(label=_("Users"), badge=lambda obj: obj.users.count(), permission="ras.view_project", weight=100)

    def get_children(self, request, parent):
        return parent.users.restrict(request.user, "view")

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        # TODO: hide this column by default? add created?
        table.columns.hide("project")
        table.columns.show("created")
        return table


@register_model_view(Project, "allocations")
class ProjectAllocationTabView(generic.ObjectChildrenView):
    actions = (BulkExport,)
    queryset = Project.objects.all()
    child_model = Allocation
    table = tables.AllocationTable
    filterset = filtersets.AllocationFilterSet
    filterset_form = forms.AllocationFilterSetForm
    template_name = "ras/project/allocations.html"
    tab = ViewTab(
        label=_("Allocations"), badge=lambda obj: obj.allocations.count(), permission="ras.view_allocation", weight=200
    )

    def get_children(self, request, parent):
        return parent.allocations.restrict(request.user, "view")


#
# Project Users
#


@register_model_view(ProjectUser, "list", path="", detail=False)
class ProjectUserListView(generic.ObjectListView):
    queryset = ProjectUser.objects.all()
    filterset = filtersets.ProjectUserFilterSet
    filterset_form = forms.ProjectUserFilterSetForm
    table = tables.ProjectUserTable


@register_model_view(ProjectUser)
class ProjectUserView(generic.ObjectView):
    queryset = ProjectUser.objects.all()


@register_model_view(ProjectUser, "add", detail=False)
@register_model_view(ProjectUser, "edit")
class ProjectUserEditView(generic.ObjectEditView):
    queryset = ProjectUser.objects.all()
    form = forms.ProjectUserForm


@register_model_view(ProjectUser, "delete")
class ProjectUserDeleteView(generic.ObjectDeleteView):
    queryset = ProjectUser.objects.all()


@register_model_view(ProjectUser, "bulk_import", path="import", detail=False)
class ProjectUserBulkImportView(generic.BulkImportView):
    queryset = ProjectUser.objects.all()
    model_form = forms.ProjectUserImportForm


@register_model_view(ProjectUser, "bulk_delete", path="delete", detail=False)
class ProjectUserBulkDeleteView(generic.BulkDeleteView):
    queryset = ProjectUser.objects.all()
    filterset = filtersets.ProjectUserFilterSet
    table = tables.ProjectUserTable
