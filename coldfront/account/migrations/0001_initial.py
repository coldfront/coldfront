# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0005_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserToken",
            fields=[],
            options={
                "verbose_name": "token",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("users.token",),
        ),
    ]
