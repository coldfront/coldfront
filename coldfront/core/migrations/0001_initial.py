# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ObjectType",
            fields=[
                (
                    "contenttype_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="object_type",
                        serialize=False,
                        to="contenttypes.contenttype",
                    ),
                ),
                ("public", models.BooleanField(default=False)),
                ("features", models.JSONField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "object type",
                "verbose_name_plural": "object types",
                "ordering": ("app_label", "model"),
            },
            bases=("contenttypes.contenttype",),
        ),
    ]
