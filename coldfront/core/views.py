# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from coldfront.core.models import ObjectChange
from coldfront.registry import register_model_view
from coldfront.utils.data import shallow_compare_dict
from coldfront.utils.query import count_related
from coldfront.views import generic
from coldfront.views.object_actions import BulkExport

from . import (
    filtersets,
    forms,
    tables,
)
from .models import Tag, TaggedItem


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
