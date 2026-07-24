# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import coldfront.models.deletion


def add_saved_filter_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    try:
        content_type = ContentType.objects.get(app_label="core", model="savedfilter")
    except ContentType.DoesNotExist:
        return

    Permission.objects.bulk_create(
        [
            Permission(
                content_type=content_type,
                codename="add_savedfilter",
                name="Can add saved filter",
            ),
            Permission(
                content_type=content_type,
                codename="change_savedfilter",
                name="Can change saved filter",
            ),
            Permission(
                content_type=content_type,
                codename="delete_savedfilter",
                name="Can delete saved filter",
            ),
            Permission(
                content_type=content_type,
                codename="view_savedfilter",
                name="Can view saved filter",
            ),
        ],
        ignore_conflicts=True,
    )


def remove_saved_filter_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    Permission.objects.filter(
        content_type__app_label="core",
        content_type__model="savedfilter",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_tableconfig"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedFilter",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="slug")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("weight", models.PositiveSmallIntegerField(default=100, verbose_name="weight")),
                ("enabled", models.BooleanField(default=True, verbose_name="enabled")),
                ("shared", models.BooleanField(default=True, verbose_name="shared")),
                ("parameters", models.JSONField(verbose_name="parameters")),
                (
                    "object_types",
                    models.ManyToManyField(
                        help_text="The object type(s) to which this filter applies.",
                        related_name="saved_filters",
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
                "verbose_name": "saved filter",
                "verbose_name_plural": "saved filters",
                "ordering": ("weight", "name"),
                "indexes": [models.Index(fields=["weight", "name"], name="core_savedfilter_weight_name")],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.RunPython(
            add_saved_filter_permissions,
            reverse_code=remove_saved_filter_permissions,
        ),
    ]
