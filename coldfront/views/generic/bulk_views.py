# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.http import HttpResponse
from django.shortcuts import render
from django_tables2.export import TableExport

from coldfront.users.permissions import get_permission_for_model
from coldfront.utils.query import reapply_model_ordering
from coldfront.views.htmx import htmx_partial
from coldfront.views.object_actions import AddObject

from .base import BaseMultiObjectView
from .mixins import ActionsMixin, TableMixin


class ObjectListView(BaseMultiObjectView, ActionsMixin, TableMixin):
    """
    Display multiple objects, all the same type, as a table.

    Attributes:
        filterset: A django-filter FilterSet that is applied to the queryset
        filterset_form: The form class used to render filter options
        actions: An iterable of ObjectAction subclasses (see ActionsMixin)
    """

    template_name = "generic/object_list.html"
    filterset = None
    filterset_form = None
    # actions = (AddObject, BulkImport, BulkExport, BulkEdit, BulkRename, BulkDelete)
    actions = (AddObject,)

    def get_required_permission(self):
        return get_permission_for_model(self.queryset.model, "view")

    #
    # Export methods
    #

    def export_yaml(self):
        """
        Export the queryset of objects as concatenated YAML documents.
        """
        yaml_data = [obj.to_yaml() for obj in self.queryset]

        return "---\n".join(yaml_data)

    def export_table(self, table, columns=None, filename=None, delimiter=None):
        """
        Export all table data in CSV format.

        Args:
            table: The Table instance to export
            columns: A list of specific columns to include. If None, all columns will be exported.
            filename: The name of the file attachment sent to the client. If None, will be determined automatically
                from the queryset model name.
            delimiter: The character used to separate columns (a comma is used by default)
        """
        exclude_columns = {"pk", "actions"}
        if columns:
            all_columns = [col_name for col_name, _ in table.selected_columns + table.available_columns]
            exclude_columns.update({col for col in all_columns if col not in columns})
        exporter = TableExport(
            export_format=TableExport.CSV,
            table=table,
            exclude_columns=exclude_columns,
        )
        return exporter.response(filename=filename or f"coldfront_{self.queryset.model._meta.verbose_name_plural}.csv")

    #
    # Request handlers
    #

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return reapply_model_ordering(qs)

    def get(self, request):
        """
        GET request handler.

        Args:
            request: The current request
        """
        model = self.queryset.model

        if self.filterset:
            self.queryset = self.filterset(request.GET, self.queryset, request=request).qs

        # Determine the available actions
        actions = self.get_permitted_actions(request.user)
        has_table_actions = any(action.multi for action in actions)

        if "export" in request.GET:
            # Export the current table view
            if request.GET["export"] == "table":
                table = self.get_table(self.queryset, request, has_table_actions)
                columns = [name for name, _ in table.selected_columns]
                return self.export_table(table, columns)

            # Check for YAML export support on the model
            elif hasattr(model, "to_yaml"):
                response = HttpResponse(self.export_yaml(), content_type="text/yaml")
                filename = "coldfront_{}.yaml".format(self.queryset.model._meta.verbose_name_plural)
                response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
                return response

            # Fall back to default table/YAML export
            else:
                table = self.get_table(self.queryset, request, has_table_actions)
                return self.export_table(table)

        # Render the objects table
        table = self.get_table(self.queryset, request, has_table_actions)

        # If this is an HTMX request, return only the rendered table HTML
        if htmx_partial(request):
            if request.GET.get("embedded", False):
                table.embedded = True
                # Hide selection checkboxes
                if "pk" in table.base_columns:
                    table.columns.hide("pk")
            return render(
                request,
                "htmx/table.html",
                {
                    "table": table,
                    "model": model,
                    "actions": actions,
                },
            )

        context = {
            "model": model,
            "table": table,
            "table_configs": None,
            "actions": actions,
            "filter_form": self.filterset_form(request.GET) if self.filterset_form else None,
            "prerequisite_model": self.get_prerequisite_model(),
            **self.get_extra_context(request),
        }

        return render(request, self.template_name, context)
