# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resource", "0003_alter_historicalresource_options_and_more"),
        ("users", "0003_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="allowed_groups",
            field=models.ManyToManyField(blank=True, to="users.group"),
        ),
    ]
