# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models

import coldfront.core.utils
import coldfront.models.deletion
import coldfront.utils.jsonschema
from coldfront.utils.migrator import migrate_allocations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_customfield"),
        ("ras", "0002_project"),
        ("tenancy", "0003_tenant_custom_field_data_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AllocationType",
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
                (
                    "schema",
                    models.JSONField(
                        blank=True,
                        null=True,
                        validators=[coldfront.utils.jsonschema.validate_schema],
                        verbose_name="schema",
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
            ],
            options={
                "verbose_name": "allocation type",
                "verbose_name_plural": "allocation types",
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Allocation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("attribute_data", models.JSONField(blank=True, null=True, verbose_name="attributes")),
                (
                    "status",
                    models.CharField(
                        choices=[("expired", "Expired"), ("active", "Active"), ("new", "New"), ("denied", "Denied")],
                        default="new",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True, verbose_name="start date")),
                ("end_date", models.DateTimeField(blank=True, null=True, verbose_name="end date")),
                ("justification", models.TextField(blank=True, null=True, verbose_name="justification")),
                ("description", models.CharField(blank=True, max_length=200, null=True, verbose_name="description")),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="allocations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="allocations", to="ras.project"
                    ),
                ),
                (
                    "resources",
                    models.ManyToManyField(
                        help_text="The resources for this allocation", related_name="allocations", to="ras.resource"
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
                        related_name="allocations",
                        to="tenancy.tenant",
                    ),
                ),
                (
                    "allocation_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="allocations",
                        to="ras.allocationtype",
                    ),
                ),
            ],
            options={
                "verbose_name": "allocation",
                "verbose_name_plural": "allocations",
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.RunPython(code=migrate_allocations, reverse_code=migrations.RunPython.noop),
    ]
