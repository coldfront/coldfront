# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_job"),
    ]

    operations = [
        # Add queue fields for the DB task backend
        migrations.AddField(
            model_name="job",
            name="task_path",
            field=models.TextField(
                blank=True,
                help_text="Dotted module path of the Task function to execute",
                verbose_name="task path",
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="args_kwargs",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=None,
                help_text="Serialized positional and keyword arguments for the task",
                verbose_name="task arguments",
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="priority",
            field=models.IntegerField(
                default=0,
                help_text="Queue priority (higher = sooner)",
                verbose_name="priority",
            ),
        ),
        migrations.AddField(
            model_name="job",
            name="worker_ids",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Worker identifiers that have processed this job",
                verbose_name="worker IDs",
            ),
        ),
    ]
