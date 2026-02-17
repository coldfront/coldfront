# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models

import coldfront.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TenantGroup",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="slug")),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="tenancy.tenantgroup",
                    ),
                ),
            ],
            options={
                "verbose_name": "tenant group",
                "verbose_name_plural": "tenant groups",
                "ordering": ["name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Tenant",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("slug", models.SlugField(max_length=100, verbose_name="slug")),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tenants",
                        to="tenancy.tenantgroup",
                    ),
                ),
            ],
            options={
                "verbose_name": "tenant",
                "verbose_name_plural": "tenants",
                "ordering": ["name"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("group", "name"),
                        name="tenancy_tenant_unique_group_name",
                        violation_error_message="Tenant name must be unique per group.",
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(("group__isnull", True)), fields=("name",), name="tenancy_tenant_unique_name"
                    ),
                    models.UniqueConstraint(
                        fields=("group", "slug"),
                        name="tenancy_tenant_unique_group_slug",
                        violation_error_message="Tenant slug must be unique per group.",
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(("group__isnull", True)), fields=("slug",), name="tenancy_tenant_unique_slug"
                    ),
                ],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
    ]
