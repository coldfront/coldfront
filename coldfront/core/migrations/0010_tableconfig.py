# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import coldfront.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_rename_core_job_created_idx_core_job_created_efa7cb_idx_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TableConfig",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                ("table", models.CharField(max_length=100, verbose_name="table")),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("weight", models.PositiveSmallIntegerField(default=1000, verbose_name="weight")),
                ("enabled", models.BooleanField(default=True, verbose_name="enabled")),
                ("shared", models.BooleanField(default=True, verbose_name="shared")),
                ("columns", models.JSONField(blank=True, default=list, null=True, verbose_name="columns")),
                ("ordering", models.JSONField(blank=True, default=list, null=True, verbose_name="ordering")),
                (
                    "object_type",
                    models.ForeignKey(
                        help_text="The table's object type",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="table_configs",
                        to="core.objecttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "table config",
                "verbose_name_plural": "table configs",
                "ordering": ("weight", "name"),
                "indexes": [models.Index(fields=["weight", "name"], name="core_tablec_weight_96d0e8_idx")],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
    ]
