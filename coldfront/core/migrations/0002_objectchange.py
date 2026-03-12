# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ObjectChange",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("time", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="time")),
                ("user_name", models.CharField(editable=False, max_length=150, verbose_name="user name")),
                ("request_id", models.UUIDField(db_index=True, editable=False, verbose_name="request ID")),
                (
                    "action",
                    models.CharField(
                        choices=[("create", "Created"), ("update", "Updated"), ("delete", "Deleted")],
                        max_length=50,
                        verbose_name="action",
                    ),
                ),
                ("changed_object_id", models.PositiveBigIntegerField()),
                ("related_object_id", models.PositiveBigIntegerField(blank=True, null=True)),
                ("object_repr", models.CharField(editable=False, max_length=200)),
                ("message", models.CharField(blank=True, editable=False, max_length=200, verbose_name="message")),
                (
                    "prechange_data",
                    models.JSONField(blank=True, editable=False, null=True, verbose_name="pre-change data"),
                ),
                (
                    "postchange_data",
                    models.JSONField(blank=True, editable=False, null=True, verbose_name="post-change data"),
                ),
                (
                    "changed_object_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="+", to="contenttypes.contenttype"
                    ),
                ),
                (
                    "related_object_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="changes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "object change",
                "verbose_name_plural": "object changes",
                "ordering": ["-time"],
                "indexes": [
                    models.Index(
                        fields=["changed_object_type", "changed_object_id"], name="core_object_changed_c227ce_idx"
                    ),
                    models.Index(
                        fields=["related_object_type", "related_object_id"], name="core_object_related_3375d6_idx"
                    ),
                ],
            },
        ),
    ]
