# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations, models

import coldfront.core.utils


class Migration(migrations.Migration):
    dependencies = [
        ("tenancy", "0002_tenant_tags_tenantgroup_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="tenant",
            name="custom_field_data",
            field=models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
        ),
        migrations.AddField(
            model_name="tenantgroup",
            name="custom_field_data",
            field=models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
        ),
    ]
