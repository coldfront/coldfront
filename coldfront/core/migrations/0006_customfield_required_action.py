# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_customfield"),
    ]

    operations = [
        migrations.AddField(
            model_name="customfield",
            name="required_action",
            field=models.CharField(
                blank=True,
                help_text="Specifies the required action that must be granted to the user in order to edit the custom field",
                max_length=50,
                null=True,
                verbose_name="Required Action",
            ),
        ),
    ]
