# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from coldfront.core.models import CustomField, CustomFieldChoiceSet, ObjectChange, Tag, TaggedItem
from coldfront.tables import ColdFrontTable, columns

from .template_code import OBJECTCHANGE_FULL_NAME, OBJECTCHANGE_OBJECT, OBJECTCHANGE_REQUEST_ID


class TagTable(ColdFrontTable):
    name = tables.Column(verbose_name=_("Name"), linkify=True)
    color = columns.ColorColumn(
        verbose_name=_("Color"),
    )
    object_types = columns.ContentTypesColumn(
        verbose_name=_("Object Types"),
    )
    owner = tables.Column(linkify=True, verbose_name=_("Owner"))

    class Meta(ColdFrontTable.Meta):
        model = Tag
        fields = (
            "pk",
            "id",
            "name",
            "items",
            "slug",
            "color",
            "weight",
            "description",
            "object_types",
            "created",
            "last_updated",
            "actions",
        )
        default_columns = ("pk", "name", "items", "slug", "color", "description")


class TaggedItemTable(ColdFrontTable):
    id = tables.Column(
        verbose_name=_("ID"),
        linkify=lambda record: record.content_object.get_absolute_url(),
        accessor="content_object__id",
    )
    content_type = columns.ContentTypeColumn(verbose_name=_("Type"))
    content_object = tables.Column(linkify=True, orderable=False, verbose_name=_("Object"))
    actions = columns.ActionsColumn(actions=())

    class Meta(ColdFrontTable.Meta):
        model = TaggedItem
        fields = ("id", "content_type", "content_object")


class ObjectChangeTable(ColdFrontTable):
    time = columns.DateTimeColumn(verbose_name=_("Time"), timespec="minutes", linkify=True)
    user_name = tables.Column(verbose_name=_("Username"))
    full_name = tables.TemplateColumn(
        accessor=tables.A("user"), template_code=OBJECTCHANGE_FULL_NAME, verbose_name=_("Full Name"), orderable=False
    )
    action = columns.ChoiceFieldColumn(
        verbose_name=_("Action"),
    )
    changed_object_type = columns.ContentTypeColumn(verbose_name=_("Type"))
    object_repr = tables.TemplateColumn(
        accessor=tables.A("changed_object"),
        template_code=OBJECTCHANGE_OBJECT,
        verbose_name=_("Object"),
        orderable=False,
    )
    request_id = tables.TemplateColumn(template_code=OBJECTCHANGE_REQUEST_ID, verbose_name=_("Request ID"))
    message = tables.Column(
        verbose_name=_("Message"),
    )
    actions = columns.ActionsColumn(actions=())

    class Meta(ColdFrontTable.Meta):
        model = ObjectChange
        fields = (
            "pk",
            "time",
            "user_name",
            "full_name",
            "action",
            "changed_object_type",
            "object_repr",
            "request_id",
            "message",
            "actions",
        )
        default_columns = (
            "pk",
            "time",
            "user_name",
            "action",
            "changed_object_type",
            "object_repr",
            "message",
            "actions",
        )


class CustomFieldChoiceSetTable(ColdFrontTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    choices = tables.TemplateColumn(
        template_code="""{% for v in value %}{{ v|split:":"|last }}{% if not forloop.last %}, {% endif %}{% endfor %}"""
    )
    choice_count = tables.TemplateColumn(
        accessor=tables.A("choices"),
        template_code="{{ value|length }}",
        orderable=False,
        verbose_name=_("Count"),
    )
    order_alphabetically = columns.BooleanColumn(
        verbose_name=_("Order Alphabetically"),
        false_mark=None,
    )

    class Meta(ColdFrontTable.Meta):
        model = CustomFieldChoiceSet
        fields = (
            "pk",
            "id",
            "name",
            "description",
            "choice_count",
            "choices",
            "order_alphabetically",
            "created",
            "last_updated",
        )
        default_columns = ("pk", "name", "choices", "choice_count", "description")


class CustomFieldTable(ColdFrontTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    object_types = columns.ContentTypesColumn(
        verbose_name=_("Object Types"),
    )
    required = columns.BooleanColumn(
        verbose_name=_("Required"),
        false_mark=None,
    )
    unique = columns.BooleanColumn(
        verbose_name=_("Validate Uniqueness"),
        false_mark=None,
    )
    ui_visible = columns.ChoiceFieldColumn(
        verbose_name=_("Visible"),
    )
    ui_editable = columns.ChoiceFieldColumn(
        verbose_name=_("Editable"),
    )
    description = columns.MarkdownColumn(
        verbose_name=_("Description"),
    )
    related_object_type = columns.ContentTypeColumn(
        verbose_name=_("Related Object Type"),
    )
    choice_set = tables.Column(
        linkify=True,
        verbose_name=_("Choice Set"),
    )
    choices = columns.ChoicesColumn(
        max_items=10,
        orderable=False,
        verbose_name=_("Choices"),
    )
    is_cloneable = columns.BooleanColumn(
        verbose_name=_("Is Cloneable"),
        false_mark=None,
    )
    validation_minimum = tables.Column(
        verbose_name=_("Minimum Value"),
    )
    validation_maximum = tables.Column(
        verbose_name=_("Maximum Value"),
    )
    validation_regex = tables.Column(
        verbose_name=_("Validation Regex"),
    )
    owner = tables.Column(linkify=True, verbose_name=_("Owner"))

    class Meta(ColdFrontTable.Meta):
        model = CustomField
        fields = (
            "pk",
            "id",
            "name",
            "object_types",
            "label",
            "type",
            "related_object_type",
            "group_name",
            "required",
            "unique",
            "default",
            "description",
            "search_weight",
            "filter_logic",
            "ui_visible",
            "ui_editable",
            "is_cloneable",
            "weight",
            "choice_set",
            "choices",
            "validation_minimum",
            "validation_maximum",
            "validation_regex",
            "comments",
            "created",
            "last_updated",
        )
        default_columns = (
            "pk",
            "name",
            "object_types",
            "label",
            "group_name",
            "type",
            "required",
            "unique",
            "description",
        )
