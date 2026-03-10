# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import coldfront.core.models.customfields
import coldfront.models.deletion
import coldfront.utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0004_customfieldchoiceset"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomField",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("longtext", "Text (long)"),
                            ("integer", "Integer"),
                            ("decimal", "Decimal"),
                            ("boolean", "Boolean (true/false)"),
                            ("date", "Date"),
                            ("datetime", "Date & time"),
                            ("select", "Selection"),
                            ("multiselect", "Multiple selection"),
                            ("object", "Object"),
                            ("multiobject", "Multiple objects"),
                        ],
                        default="text",
                        help_text="The type of data this custom field holds",
                        max_length=50,
                        verbose_name="type",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Internal field name",
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                flags=re.RegexFlag["IGNORECASE"],
                                message="Only alphanumeric characters and underscores are allowed.",
                                regex="^[a-z0-9_]+$",
                            ),
                            django.core.validators.RegexValidator(
                                flags=re.RegexFlag["IGNORECASE"],
                                inverse_match=True,
                                message="Double underscores are not permitted in custom field names.",
                                regex="__",
                            ),
                        ],
                        verbose_name="name",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text="Name of the field as displayed to users (if not provided, 'the field's name will be used)",
                        max_length=50,
                        verbose_name="label",
                    ),
                ),
                (
                    "group_name",
                    models.CharField(
                        blank=True,
                        help_text="Custom fields within the same group will be displayed together",
                        max_length=50,
                        verbose_name="group name",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                (
                    "required",
                    models.BooleanField(
                        default=False,
                        help_text="This field is required when creating new objects or editing an existing object.",
                        verbose_name="required",
                    ),
                ),
                (
                    "unique",
                    models.BooleanField(
                        default=False,
                        help_text="The value of this field must be unique for the assigned object",
                        verbose_name="must be unique",
                    ),
                ),
                (
                    "search_weight",
                    models.PositiveSmallIntegerField(
                        default=1000,
                        help_text="Weighting for search. Lower values are considered more important. Fields with a search weight of zero will be ignored.",
                        verbose_name="search weight",
                    ),
                ),
                (
                    "filter_logic",
                    models.CharField(
                        choices=[("disabled", "Disabled"), ("loose", "Loose"), ("exact", "Exact")],
                        default="loose",
                        help_text="Loose matches any instance of a given string; exact matches the entire field.",
                        max_length=50,
                        verbose_name="filter logic",
                    ),
                ),
                (
                    "default",
                    models.JSONField(
                        blank=True,
                        help_text='Default value for the field (must be a JSON value). Encapsulate strings with double quotes (e.g. "Foo").',
                        null=True,
                        verbose_name="default",
                    ),
                ),
                (
                    "related_object_filter",
                    models.JSONField(
                        blank=True,
                        help_text='Filter the object selection choices using a query_params dict (must be a JSON value).Encapsulate strings with double quotes (e.g. "Foo").',
                        null=True,
                    ),
                ),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text="Fields with higher weights appear lower in a form.",
                        verbose_name="display weight",
                    ),
                ),
                (
                    "validation_minimum",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        help_text="Minimum allowed value (for numeric fields)",
                        max_digits=16,
                        null=True,
                        verbose_name="minimum value",
                    ),
                ),
                (
                    "validation_maximum",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        help_text="Maximum allowed value (for numeric fields)",
                        max_digits=16,
                        null=True,
                        verbose_name="maximum value",
                    ),
                ),
                (
                    "validation_regex",
                    models.CharField(
                        blank=True,
                        help_text="Regular expression to enforce on text field values. Use ^ and $ to force matching of entire string. For example, <code>^[A-Z]{3}$</code> will limit values to exactly three uppercase letters.",
                        max_length=500,
                        validators=[coldfront.utils.validators.validate_regex],
                        verbose_name="validation regex",
                    ),
                ),
                (
                    "ui_visible",
                    models.CharField(
                        choices=[("always", "Always"), ("if-set", "If set"), ("hidden", "Hidden")],
                        default="always",
                        help_text="Specifies whether the custom field is displayed in the UI",
                        max_length=50,
                        verbose_name="UI visible",
                    ),
                ),
                (
                    "ui_editable",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No"), ("hidden", "Hidden")],
                        default="yes",
                        help_text="Specifies whether the custom field value can be edited in the UI",
                        max_length=50,
                        verbose_name="UI editable",
                    ),
                ),
                (
                    "is_cloneable",
                    models.BooleanField(
                        default=False,
                        help_text="Replicate this value when cloning objects",
                        verbose_name="is cloneable",
                    ),
                ),
                ("comments", models.TextField(blank=True, verbose_name="comments")),
                (
                    "choice_set",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="choices_for",
                        to="core.customfieldchoiceset",
                        verbose_name="choice set",
                    ),
                ),
                (
                    "object_types",
                    models.ManyToManyField(
                        help_text="The object(s) to which this field applies.",
                        related_name="custom_fields",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "related_object_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="The type of ColdFront object this field maps to (for object fields)",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "custom field",
                "verbose_name_plural": "custom fields",
                "ordering": ["group_name", "weight", "name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
            managers=[
                ("objects", coldfront.core.models.customfields.CustomFieldManager()),
            ],
        ),
    ]
