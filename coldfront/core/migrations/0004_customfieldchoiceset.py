# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django_jsonform.models.fields
from django.db import migrations, models

import coldfront.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_tag_taggeditem"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomFieldChoiceSet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("choices", django_jsonform.models.fields.JSONField()),
                (
                    "order_alphabetically",
                    models.BooleanField(default=False, help_text="Choices are automatically ordered alphabetically"),
                ),
            ],
            options={
                "verbose_name": "custom field choice set",
                "verbose_name_plural": "custom field choice sets",
                "ordering": ("name",),
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
    ]
