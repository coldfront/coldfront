# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import coldfront.core.utils


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_job_task_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="job",
            new_name="core_job_created_efa7cb_idx",
            old_name="core_job_created_idx",
        ),
        migrations.RenameIndex(
            model_name="job",
            new_name="core_job_object__c664ac_idx",
            old_name="core_job_object_idx",
        ),
        migrations.AlterField(
            model_name="job",
            name="args_kwargs",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                help_text="Serialized positional and keyword arguments for the task",
                verbose_name="task arguments",
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="data",
            field=models.JSONField(
                blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name="data"
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="id",
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="job",
            name="log_entries",
            field=models.JSONField(
                blank=True,
                decoder=coldfront.core.utils.JobLogDecoder,
                default=list,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                verbose_name="log entries",
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
