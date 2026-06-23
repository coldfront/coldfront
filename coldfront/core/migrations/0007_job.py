# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.core.validators import MinValueValidator
from django.db import migrations, models


def update_object_types(apps, schema_editor):
    """
    Create ObjectType entries for the Job model.
    """
    ObjectType = apps.get_model("core.ObjectType")
    db_alias = schema_editor.connection.alias

    ObjectType.objects.using(db_alias).create(
        app_label="core",
        model="job",
        public=True,
        features={"custom_fields": False, "tags": False, "jobs": False},
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_customfield_required_action"),
    ]

    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "object_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.CASCADE,
                        related_name="jobs",
                        to="contenttypes.ContentType",
                    ),
                ),
                ("object_id", models.PositiveBigIntegerField(blank=True, null=True)),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="created")),
                ("scheduled", models.DateTimeField(blank=True, null=True, verbose_name="scheduled")),
                (
                    "interval",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Recurrence interval (in minutes)",
                        null=True,
                        validators=[MinValueValidator(1)],
                        verbose_name="interval",
                    ),
                ),
                ("started", models.DateTimeField(blank=True, null=True, verbose_name="started")),
                ("completed", models.DateTimeField(blank=True, null=True, verbose_name="completed")),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.SET_NULL,
                        related_name="+",
                        to="users.User",
                        verbose_name="user",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ["pending", "Pending"],
                            ["scheduled", "Scheduled"],
                            ["running", "Running"],
                            ["completed", "Completed"],
                            ["failed", "Failed"],
                            ["errored", "Errored"],
                        ],
                        default="pending",
                        max_length=30,
                        verbose_name="status",
                    ),
                ),
                ("data", models.JSONField(blank=True, null=True, verbose_name="data")),
                ("error", models.TextField(blank=True, editable=False, verbose_name="error")),
                ("job_id", models.UUIDField(unique=True, verbose_name="job ID")),
                (
                    "queue_name",
                    models.CharField(
                        blank=True,
                        help_text="Name of the queue in which this job was enqueued",
                        max_length=100,
                        verbose_name="queue name",
                    ),
                ),
                (
                    "notifications",
                    models.CharField(
                        choices=[
                            ["always", "Always"],
                            ["on_failure", "On failure"],
                            ["never", "Never"],
                        ],
                        default="always",
                        max_length=30,
                        verbose_name="notifications",
                    ),
                ),
                (
                    "log_entries",
                    models.JSONField(
                        blank=True,
                        default=list,
                        verbose_name="log entries",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
                "verbose_name": "job",
                "verbose_name_plural": "jobs",
            },
        ),
        migrations.AddIndex(
            model_name="Job",
            index=models.Index(fields=["-created"], name="core_job_created_idx"),
        ),
        migrations.AddIndex(
            model_name="Job",
            index=models.Index(
                fields=["object_type", "object_id"],
                name="core_job_object_idx",
            ),
        ),
        migrations.RunPython(
            code=update_object_types,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
