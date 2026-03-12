# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
from django.db import migrations, models

import coldfront.models.deletion
import coldfront.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0002_objectchange"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("slug", models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name="slug")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("color", coldfront.models.fields.ColorField(default="9e9e9e", max_length=6, verbose_name="color")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("weight", models.PositiveSmallIntegerField(default=1000, verbose_name="weight")),
                (
                    "object_types",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The object type(s) to which this tag can be applied.",
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "tag",
                "verbose_name_plural": "tags",
                "ordering": ("weight", "name"),
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="TaggedItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.IntegerField(db_index=True, verbose_name="object ID")),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_tagged_items",
                        to="contenttypes.contenttype",
                        verbose_name="content type",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_items",
                        to="core.tag",
                    ),
                ),
            ],
            options={
                "verbose_name": "tagged item",
                "verbose_name_plural": "tagged items",
                "indexes": [models.Index(fields=["content_type", "object_id"], name="core_tagged_content_0b937e_idx")],
            },
        ),
    ]
