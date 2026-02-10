# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0002_alter_user_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                (
                    "permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="groups",
                        related_query_name="group",
                        to="auth.permission",
                        verbose_name="permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "group",
                "verbose_name_plural": "groups",
                "ordering": ("name",),
            },
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.RunSQL(
            sql="INSERT INTO users_group (id, name, description) SELECT id, name, '' AS description FROM auth_group;",
        ),
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="users", related_query_name="user", to="users.group", verbose_name="groups"
            ),
        ),
        migrations.RunSQL(
            sql="DELETE from auth_group",
        ),
    ]
