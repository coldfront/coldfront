# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db import migrations, models

import coldfront.users.models.users


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("users", "0003_group"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="group",
            managers=[
                ("objects", coldfront.users.models.users.GroupManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", coldfront.users.models.users.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="ObjectPermission",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("enabled", models.BooleanField(default=True, verbose_name="enabled")),
                (
                    "actions",
                    models.JSONField(
                        blank=True,
                        help_text="The list of actions granted by this permission",
                        null=True,
                        verbose_name="actions",
                    ),
                ),
                (
                    "constraints",
                    models.JSONField(
                        blank=True,
                        help_text="Queryset filter matching the applicable objects of the selected type(s)",
                        null=True,
                        verbose_name="constraints",
                    ),
                ),
                (
                    "object_types",
                    models.ManyToManyField(related_name="object_permissions", to="contenttypes.contenttype"),
                ),
            ],
            options={
                "verbose_name": "permission",
                "verbose_name_plural": "permissions",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="group",
            name="object_permissions",
            field=models.ManyToManyField(blank=True, related_name="groups", to="users.objectpermission"),
        ),
        migrations.AddField(
            model_name="user",
            name="object_permissions",
            field=models.ManyToManyField(blank=True, related_name="users", to="users.objectpermission"),
        ),
    ]
