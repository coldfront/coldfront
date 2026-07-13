# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ras", "0001_initial"),
        ("users", "0006_alter_token_pepper_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="group",
            field=models.ForeignKey(
                blank=True,
                help_text="The Group associated with this project. Users added to the project are automatically added to this group.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="projects",
                to="users.group",
                verbose_name="group",
            ),
        ),
    ]
