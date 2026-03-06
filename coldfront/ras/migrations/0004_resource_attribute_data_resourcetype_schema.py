# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db import migrations, models

import coldfront.utils.jsonschema


class Migration(migrations.Migration):
    dependencies = [
        ("ras", "0003_allocationtype_allocation"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="attribute_data",
            field=models.JSONField(blank=True, null=True, verbose_name="attributes"),
        ),
        migrations.AddField(
            model_name="resourcetype",
            name="schema",
            field=models.JSONField(
                blank=True, null=True, validators=[coldfront.utils.jsonschema.validate_schema], verbose_name="schema"
            ),
        ),
    ]
