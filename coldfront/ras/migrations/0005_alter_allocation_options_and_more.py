# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ras", "0004_resource_attribute_data_resourcetype_schema"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="allocation",
            options={"ordering": ["start_date"], "verbose_name": "allocation", "verbose_name_plural": "allocations"},
        ),
        migrations.AlterModelOptions(
            name="allocationtype",
            options={
                "ordering": ["name"],
                "verbose_name": "allocation type",
                "verbose_name_plural": "allocation types",
            },
        ),
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["name"], "verbose_name": "project", "verbose_name_plural": "projects"},
        ),
        migrations.AlterModelOptions(
            name="resource",
            options={"ordering": ["name"], "verbose_name": "resource", "verbose_name_plural": "resources"},
        ),
        migrations.AlterModelOptions(
            name="resourcetype",
            options={"ordering": ["name"], "verbose_name": "resource type", "verbose_name_plural": "resource types"},
        ),
        migrations.RemoveField(
            model_name="resourcetype",
            name="resource_count",
        ),
    ]
