# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ras", "0006_alter_project_owner_projectuser"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="projectuser",
            unique_together={("user", "project")},
        ),
    ]
