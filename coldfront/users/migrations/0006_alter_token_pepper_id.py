# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="pepper_id",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="ID of the cryptographic pepper used to hash the token",
                null=True,
                verbose_name="pepper ID",
            ),
        ),
    ]
