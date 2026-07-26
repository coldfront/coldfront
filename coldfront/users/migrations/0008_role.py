# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add the Role model for role-based permission management.
    """

    dependencies = [
        ("users", "0007_userconfig"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="name"),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=200, verbose_name="description"),
                ),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text="Weight is used for ordering and precedence resolution.",
                        verbose_name="weight",
                    ),
                ),
            ],
            options={
                "ordering": ("weight", "name"),
                "verbose_name": "role",
                "verbose_name_plural": "roles",
            },
        ),
        migrations.AddField(
            model_name="role",
            name="object_permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="roles",
                to="users.ObjectPermission",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="roles",
            field=models.ManyToManyField(
                blank=True,
                related_name="users",
                to="users.Role",
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="roles",
            field=models.ManyToManyField(
                blank=True,
                related_name="groups",
                to="users.Role",
            ),
        ),
    ]
