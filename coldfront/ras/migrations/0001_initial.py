# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
import django.db.models.functions.text
import mptt.fields
import taggit.managers
from django.conf import settings
from django.db import migrations, models

import coldfront.core.utils
import coldfront.models.deletion
import coldfront.models.fields
import coldfront.utils.jsonschema


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0006_customfield_required_action"),
        ("tenancy", "0003_tenant_custom_field_data_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("slug", coldfront.models.fields.AutoSlugField(blank=True, unique=True, verbose_name="slug")),
                (
                    "status",
                    models.CharField(
                        choices=[("archived", "Archived"), ("active", "Active")],
                        default="active",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="owned_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="projects",
                        to="tenancy.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "project",
                "verbose_name_plural": "projects",
                "ordering": ["name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("attribute_data", models.JSONField(blank=True, null=True, verbose_name="attributes")),
                ("slug", models.SlugField(max_length=100, verbose_name="slug")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("offline", "Offline"),
                            ("active", "Active"),
                            ("planned", "Planned"),
                            ("staged", "Staged"),
                            ("decommissioning", "Decommissioning"),
                        ],
                        default="active",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
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
                        to="ras.resource",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="resources",
                        to="tenancy.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "resource",
                "verbose_name_plural": "resources",
                "ordering": ["name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Allocation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("attribute_data", models.JSONField(blank=True, null=True, verbose_name="attributes")),
                ("slug", coldfront.models.fields.AutoSlugField(blank=True, unique=True, verbose_name="slug")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("active", "Active"),
                            ("denied", "Denied"),
                            ("expired", "Expired"),
                            ("approved", "Approved"),
                            ("revoked", "Revoked"),
                            ("renew", "Renew"),
                        ],
                        default="new",
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True, verbose_name="start date")),
                ("end_date", models.DateTimeField(blank=True, null=True, verbose_name="end date")),
                ("justification", models.TextField(blank=True, null=True, verbose_name="justification")),
                ("description", models.CharField(blank=True, max_length=200, null=True, verbose_name="description")),
                ("comments", models.TextField(blank=True, verbose_name="comments")),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="owned_allocations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="allocations",
                        to="tenancy.tenant",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="allocations", to="ras.project"
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        help_text="The resource for this allocation",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="allocations",
                        to="ras.resource",
                    ),
                ),
            ],
            options={
                "verbose_name": "allocation",
                "verbose_name_plural": "allocations",
                "ordering": ["start_date"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ResourceType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                (
                    "schema",
                    models.JSONField(
                        blank=True,
                        null=True,
                        validators=[coldfront.utils.jsonschema.validate_schema],
                        verbose_name="schema",
                    ),
                ),
                ("is_default", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                (
                    "allocation_schema",
                    models.JSONField(
                        blank=True,
                        null=True,
                        validators=[coldfront.utils.jsonschema.validate_schema],
                        verbose_name="schema",
                    ),
                ),
                ("slug", models.SlugField(max_length=100, unique=True, verbose_name="slug")),
                ("color", coldfront.models.fields.ColorField(default="9e9e9e", max_length=6, verbose_name="color")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "verbose_name": "resource type",
                "verbose_name_plural": "resource types",
                "ordering": ["name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.AddField(
            model_name="resource",
            name="resource_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="resources",
                to="ras.resourcetype",
            ),
        ),
        migrations.CreateModel(
            name="AllocationUser",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                (
                    "allocation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="users", to="ras.allocation"
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="allocations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "allocation user",
                "verbose_name_plural": "allocation users",
                "ordering": ["id"],
                "unique_together": {("user", "allocation")},
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProjectUser",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="users", to="ras.project"
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="core.TaggedItem",
                        to="core.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "project user",
                "verbose_name_plural": "project users",
                "ordering": ["id"],
                "unique_together": {("user", "project")},
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name="resource",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                models.F("parent"),
                models.F("tenant"),
                name="ras_resource_unique_name_parent_tenant",
            ),
        ),
        migrations.AddConstraint(
            model_name="resource",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                models.F("parent"),
                condition=models.Q(("tenant__isnull", True)),
                name="ras_resource_unique_name_parent",
                violation_error_message="Resource name must be unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="resource",
            constraint=models.UniqueConstraint(
                condition=models.Q(("parent__isnull", True), ("tenant__isnull", True)),
                fields=("name",),
                name="ras_resource_name",
                violation_error_message="A top-level resource with this name already exists.",
            ),
        ),
        migrations.AddConstraint(
            model_name="resource",
            constraint=models.UniqueConstraint(fields=("parent", "slug"), name="ras_resource_parent_slug"),
        ),
        migrations.AddConstraint(
            model_name="resource",
            constraint=models.UniqueConstraint(
                condition=models.Q(("parent__isnull", True)),
                fields=("slug",),
                name="ras_resource_slug",
                violation_error_message="A top-level resource with this slug already exists.",
            ),
        ),
    ]
