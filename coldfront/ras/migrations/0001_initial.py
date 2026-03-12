# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models

import coldfront.core.utils
import coldfront.models.deletion
import coldfront.models.fields
from coldfront.utils.migrator import migrate_resources


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0005_customfield"),
        ("tenancy", "0003_tenant_custom_field_data_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResourceType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="slug")),
                ("color", coldfront.models.fields.ColorField(default="9e9e9e", max_length=6, verbose_name="color")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "verbose_name": "resource type",
                "verbose_name_plural": "resource types",
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("offline", "Offline"),
                            ("active", "Active"),
                            ("planned", "Planned"),
                            ("staged", "Staged"),
                            ("decommissioning", "Decommissioning"),
                        ],
                        default="active",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="resources",
                        to="tenancy.tenant",
                    ),
                ),
                (
                    "resource_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="resources", to="ras.resourcetype"
                    ),
                ),
            ],
            options={
                "verbose_name": "resource",
                "verbose_name_plural": "resources",
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.RunPython(code=migrate_resources, reverse_code=migrations.RunPython.noop),
    ]
