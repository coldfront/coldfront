# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import View
from django_cotton import render_component

from coldfront.registry import register_model_view
from coldfront.tables.paginator import EnhancedPaginator, get_paginate_count
from coldfront.utils.data import shallow_compare_dict
from coldfront.utils.query import count_related
from coldfront.views import generic
from coldfront.views.htmx import htmx_partial
from coldfront.views.object_actions import BulkExport

from . import (
    filtersets,
    forms,
    tables,
)
from .models import CustomField, CustomFieldChoiceSet, ObjectChange, Tag, TaggedItem
from .plugins import get_local_plugins
from .tables import CatalogPluginTable, PluginVersionTable


@register_model_view(Tag, "list", path="", detail=False)
class TagListView(generic.ObjectListView):
    queryset = Tag.objects.annotate(items=count_related(TaggedItem, "tag"))
    filterset = filtersets.TagFilterSet
    filterset_form = forms.TagFilterForm
    table = tables.TagTable


@register_model_view(Tag)
class TagView(generic.ObjectView):
    queryset = Tag.objects.all()

    def get_extra_context(self, request, instance):
        tagged_items = TaggedItem.objects.filter(tag=instance)
        taggeditem_table = tables.TaggedItemTable(data=tagged_items, orderable=False)
        taggeditem_table.configure(request)

        object_types = [
            {"content_type": ContentType.objects.get(pk=ti["content_type"]), "item_count": ti["item_count"]}
            for ti in tagged_items.values("content_type").annotate(item_count=Count("pk"))
        ]

        return {
            "taggeditem_table": taggeditem_table,
            "tagged_item_count": tagged_items.count(),
            "object_types": object_types,
        }


@register_model_view(Tag, "add", detail=False)
@register_model_view(Tag, "edit")
class TagEditView(generic.ObjectEditView):
    queryset = Tag.objects.all()
    form = forms.TagForm


@register_model_view(Tag, "delete")
class TagDeleteView(generic.ObjectDeleteView):
    queryset = Tag.objects.all()


@register_model_view(Tag, "bulk_import", path="import", detail=False)
class TagBulkImportView(generic.BulkImportView):
    queryset = Tag.objects.all()
    model_form = forms.TagImportForm


@register_model_view(Tag, "bulk_delete", path="delete", detail=False)
class TagBulkDeleteView(generic.BulkDeleteView):
    queryset = Tag.objects.annotate(
        items=count_related(TaggedItem, "tag"),
    )
    table = tables.TagTable


#
# Change logging
#


@register_model_view(ObjectChange, "list", path="", detail=False)
class ObjectChangeListView(generic.ObjectListView):
    queryset = None
    filterset = filtersets.ObjectChangeFilterSet
    filterset_form = forms.ObjectChangeFilterForm
    table = tables.ObjectChangeTable
    template_name = "core/objectchange_list.html"
    actions = (BulkExport,)

    def get_queryset(self, request):
        return ObjectChange.objects.valid_models()


@register_model_view(ObjectChange)
class ObjectChangeView(generic.ObjectView):
    queryset = None

    def get_queryset(self, request):
        return ObjectChange.objects.valid_models()

    def get_extra_context(self, request, instance):
        related_changes = (
            ObjectChange.objects.valid_models()
            .restrict(request.user, "view")
            .filter(request_id=instance.request_id)
            .exclude(pk=instance.pk)
        )
        related_changes_table = tables.ObjectChangeTable(data=related_changes[:50], orderable=False)
        related_changes_table.configure(request)

        objectchanges = (
            ObjectChange.objects.valid_models()
            .restrict(request.user, "view")
            .filter(
                changed_object_type=instance.changed_object_type,
                changed_object_id=instance.changed_object_id,
            )
        )

        next_change = objectchanges.filter(time__gt=instance.time).order_by("time").first()
        prev_change = objectchanges.filter(time__lt=instance.time).order_by("-time").first()

        if not instance.prechange_data and instance.action in ["update", "delete"] and prev_change:
            non_atomic_change = True
            prechange_data = prev_change.postchange_data_clean
        else:
            non_atomic_change = False
            prechange_data = instance.prechange_data_clean

        if prechange_data and instance.postchange_data:
            diff_added = shallow_compare_dict(
                prechange_data or dict(),
                instance.postchange_data_clean or dict(),
                exclude=["last_updated"],
            )
            diff_removed = {x: prechange_data.get(x) for x in diff_added} if prechange_data else {}
        else:
            diff_added = None
            diff_removed = None

        return {
            "diff_added": diff_added,
            "diff_removed": diff_removed,
            "next_change": next_change,
            "prev_change": prev_change,
            "related_changes_table": related_changes_table,
            "related_changes_count": related_changes.count(),
            "non_atomic_change": non_atomic_change,
        }


#
# Custom field choices
#


@register_model_view(CustomFieldChoiceSet, "list", path="", detail=False)
class CustomFieldChoiceSetListView(generic.ObjectListView):
    queryset = CustomFieldChoiceSet.objects.all()
    filterset = filtersets.CustomFieldChoiceSetFilterSet
    filterset_form = forms.CustomFieldChoiceSetFilterForm
    table = tables.CustomFieldChoiceSetTable


@register_model_view(CustomFieldChoiceSet)
class CustomFieldChoiceSetView(generic.ObjectView):
    queryset = CustomFieldChoiceSet.objects.all()

    def get_extra_context(self, request, instance):

        # Paginate choices list
        per_page = get_paginate_count(request)
        try:
            page_number = request.GET.get("page", 1)
        except ValueError:
            page_number = 1
        paginator = EnhancedPaginator(instance.choices, per_page)
        try:
            choices = paginator.page(page_number)
        except EmptyPage:
            choices = paginator.page(paginator.num_pages)

        return {
            "paginator": paginator,
            "choices": choices,
        }


@register_model_view(CustomFieldChoiceSet, "add", detail=False)
@register_model_view(CustomFieldChoiceSet, "edit")
class CustomFieldChoiceSetEditView(generic.ObjectEditView):
    queryset = CustomFieldChoiceSet.objects.all()
    form = forms.CustomFieldChoiceSetForm


@register_model_view(CustomFieldChoiceSet, "delete")
class CustomFieldChoiceSetDeleteView(generic.ObjectDeleteView):
    queryset = CustomFieldChoiceSet.objects.all()


@register_model_view(CustomFieldChoiceSet, "bulk_import", path="import", detail=False)
class CustomFieldChoiceSetBulkImportView(generic.BulkImportView):
    queryset = CustomFieldChoiceSet.objects.all()
    model_form = forms.CustomFieldChoiceSetImportForm


@register_model_view(CustomFieldChoiceSet, "bulk_delete", path="delete", detail=False)
class CustomFieldChoiceSetBulkDeleteView(generic.BulkDeleteView):
    queryset = CustomFieldChoiceSet.objects.all()
    filterset = filtersets.CustomFieldChoiceSetFilterSet
    table = tables.CustomFieldChoiceSetTable


#
# Custom fields
#


@register_model_view(CustomField, "list", path="", detail=False)
class CustomFieldListView(generic.ObjectListView):
    queryset = CustomField.objects.select_related("choice_set")
    filterset = filtersets.CustomFieldFilterSet
    filterset_form = forms.CustomFieldFilterForm
    table = tables.CustomFieldTable


@register_model_view(CustomField)
class CustomFieldView(generic.ObjectView):
    queryset = CustomField.objects.select_related("choice_set")

    def get_extra_context(self, request, instance):
        related_models = ()

        for object_type in instance.object_types.all():
            related_models += (
                object_type.model_class()
                .objects.restrict(request.user, "view")
                .exclude(
                    Q(**{f"custom_field_data__{instance.name}": ""})
                    | Q(**{f"custom_field_data__{instance.name}": None})
                ),
            )

        return {"related_models": related_models}


@register_model_view(CustomField, "add", detail=False)
@register_model_view(CustomField, "edit")
class CustomFieldEditView(generic.ObjectEditView):
    queryset = CustomField.objects.select_related("choice_set")
    form = forms.CustomFieldForm


@register_model_view(CustomField, "delete")
class CustomFieldDeleteView(generic.ObjectDeleteView):
    queryset = CustomField.objects.select_related("choice_set")


@register_model_view(CustomField, "bulk_import", path="import", detail=False)
class CustomFieldBulkImportView(generic.BulkImportView):
    queryset = CustomField.objects.select_related("choice_set")
    model_form = forms.CustomFieldImportForm


@register_model_view(CustomField, "bulk_delete", path="delete", detail=False)
class CustomFieldBulkDeleteView(generic.BulkDeleteView):
    queryset = CustomField.objects.select_related("choice_set")
    filterset = filtersets.CustomFieldFilterSet
    table = tables.CustomFieldTable


#
# Plugins
#


class BasePluginView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get_plugins(self, request):
        plugins = {}
        return get_local_plugins(plugins)


class PluginListView(BasePluginView):
    def get(self, request):
        q = request.GET.get("q", None)

        plugins = self.get_plugins(request).values()
        if q:
            plugins = [obj for obj in plugins if q.casefold() in obj.title_short.casefold()]

        plugins = [plugin for plugin in plugins if not plugin.hidden]

        table = CatalogPluginTable(plugins)
        table.configure(request)

        # If this is an HTMX request, return only the rendered table HTML
        if htmx_partial(request):
            return render_component(
                request,
                "table.htmx",
                table=table,
            )

        return render(
            request,
            "core/plugin_list.html",
            {
                "table": table,
            },
        )


class PluginView(BasePluginView):
    def get(self, request, name):

        plugins = self.get_plugins(request)
        if name not in plugins:
            raise Http404(_("Plugin {name} not found").format(name=name))
        plugin = plugins[name]

        table = PluginVersionTable(plugin.release_recent_history)
        table.configure(request)

        return render(
            request,
            "core/plugin.html",
            {
                "plugin": plugin,
                "table": table,
            },
        )
