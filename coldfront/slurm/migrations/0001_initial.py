# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models

import coldfront.core.utils
import coldfront.models.deletion
import coldfront.utils.jsonschema


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0009_rename_core_job_created_idx_core_job_created_efa7cb_idx_and_more"),
        ("ras", "0002_remove_project_status_project_group"),
        ("tenancy", "0003_tenant_custom_field_data_and_more"),
        ("users", "0006_alter_token_pepper_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SlurmCluster",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "schema",
                    models.JSONField(
                        blank=True,
                        null=True,
                        validators=[coldfront.utils.jsonschema.validate_schema],
                        verbose_name="schema",
                    ),
                ),
                (
                    "locked",
                    models.BooleanField(
                        default=False,
                        help_text="Prevent users from submitting allocations for this resource.",
                        verbose_name="locked",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("fairshare", models.PositiveIntegerField(blank=True, default=1, verbose_name="fairshare")),
                ("features", models.JSONField(blank=True, default=list, null=True, verbose_name="features")),
                (
                    "classification",
                    models.CharField(blank=True, max_length=50, null=True, verbose_name="classification"),
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
                        related_name="slurm_clusters",
                        to="tenancy.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "slurm cluster",
                "verbose_name_plural": "slurm clusters",
                "ordering": ["name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SlurmAccount",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "fairshare",
                    models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name="fairshare"),
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
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="accounts",
                        to="slurm.slurmcluster",
                        verbose_name="cluster",
                    ),
                ),
            ],
            options={
                "verbose_name": "slurm account",
                "verbose_name_plural": "slurm accounts",
                "ordering": ["cluster__name", "name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SlurmQOS",
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
                "verbose_name": "slurm qos",
                "verbose_name_plural": "slurm qos",
                "ordering": ["name"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.AddField(
            model_name="slurmcluster",
            name="default_qos",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="default_for_clusters",
                to="slurm.slurmqos",
                verbose_name="default QOS",
            ),
        ),
        migrations.AddField(
            model_name="slurmcluster",
            name="qos_list",
            field=models.ManyToManyField(
                blank=True,
                related_name="clusters",
                related_query_name="cluster",
                to="slurm.slurmqos",
                verbose_name="QOS list",
            ),
        ),
        migrations.CreateModel(
            name="SlurmAssociation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("fairshare", models.PositiveIntegerField(blank=True, default=1, verbose_name="fairshare")),
                ("max_jobs", models.PositiveIntegerField(blank=True, null=True, verbose_name="max jobs")),
                ("max_submit_jobs", models.PositiveIntegerField(blank=True, null=True, verbose_name="max submit jobs")),
                ("max_tres_per_job", models.JSONField(blank=True, null=True, verbose_name="max TRES per job")),
                (
                    "max_tres_mins_per_job",
                    models.JSONField(blank=True, null=True, verbose_name="max TRES minutes per job"),
                ),
                (
                    "max_wall_duration_per_job",
                    models.DurationField(blank=True, null=True, verbose_name="max wall duration per job"),
                ),
                (
                    "allocation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="slurm_associations",
                        to="ras.allocation",
                        unique=True,
                        verbose_name="allocation",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="child_associations",
                        to="slurm.slurmaccount",
                        verbose_name="parent account",
                    ),
                ),
                (
                    "slurm_account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="associations",
                        to="slurm.slurmaccount",
                        verbose_name="Slurm account",
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
                    "default_qos",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="associations",
                        to="slurm.slurmqos",
                        verbose_name="default QOS",
                    ),
                ),
            ],
            options={
                "verbose_name": "slurm association",
                "verbose_name_plural": "slurm associations",
                "ordering": ["allocation__slug"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.AddField(
            model_name="slurmaccount",
            name="qos_list",
            field=models.ManyToManyField(
                blank=True,
                related_name="accounts",
                related_query_name="account",
                to="slurm.slurmqos",
                verbose_name="QOS list",
            ),
        ),
        migrations.CreateModel(
            name="SlurmUser",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                (
                    "default_wckey",
                    models.CharField(blank=True, max_length=100, null=True, verbose_name="default wckey"),
                ),
                (
                    "admin_level",
                    models.SmallIntegerField(
                        blank=True,
                        choices=[(0, "None"), (1, "Operator"), (2, "Admin")],
                        null=True,
                        verbose_name="admin level",
                    ),
                ),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="users",
                        to="slurm.slurmcluster",
                        verbose_name="cluster",
                    ),
                ),
                (
                    "default_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="default_for_users",
                        to="slurm.slurmaccount",
                        verbose_name="default account",
                    ),
                ),
                (
                    "default_qos",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="default_for_users",
                        to="slurm.slurmqos",
                        verbose_name="default QOS",
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
                        related_name="slurm_users",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "slurm user",
                "verbose_name_plural": "slurm users",
                "ordering": ["cluster__name", "user__username"],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SlurmPartition",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True, verbose_name="created")),
                ("last_updated", models.DateTimeField(auto_now=True, null=True, verbose_name="last updated")),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=coldfront.core.utils.CustomFieldJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "schema",
                    models.JSONField(
                        blank=True,
                        null=True,
                        validators=[coldfront.utils.jsonschema.validate_schema],
                        verbose_name="schema",
                    ),
                ),
                (
                    "locked",
                    models.BooleanField(
                        default=False,
                        help_text="Prevent users from submitting allocations for this resource.",
                        verbose_name="locked",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("max_jobs", models.PositiveIntegerField(blank=True, null=True, verbose_name="max jobs")),
                ("max_submit_jobs", models.PositiveIntegerField(blank=True, null=True, verbose_name="max submit jobs")),
                ("max_tres_per_job", models.JSONField(blank=True, null=True, verbose_name="max TRES per job")),
                ("max_tres_per_node", models.JSONField(blank=True, null=True, verbose_name="max TRES per node")),
                (
                    "max_tres_mins_per_job",
                    models.JSONField(blank=True, null=True, verbose_name="max TRES minutes per job"),
                ),
                (
                    "max_wall_duration_per_job",
                    models.DurationField(blank=True, null=True, verbose_name="max wall duration per job"),
                ),
                ("fairshare", models.PositiveIntegerField(blank=True, default=1, verbose_name="fairshare")),
                (
                    "nodes",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Comma-separated node list for this partition (e.g., node[01-64]).",
                        verbose_name="nodes",
                    ),
                ),
                (
                    "allow_accounts",
                    models.ManyToManyField(
                        blank=True,
                        related_name="allowed_partitions",
                        related_query_name="allowed_partition",
                        to="slurm.slurmaccount",
                        verbose_name="allowed accounts",
                    ),
                ),
                (
                    "allow_groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="allowed_partitions",
                        related_query_name="allowed_partition",
                        to="users.group",
                        verbose_name="allowed groups",
                    ),
                ),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="partitions",
                        to="slurm.slurmcluster",
                        verbose_name="cluster",
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
                    "qos_list",
                    models.ManyToManyField(
                        blank=True,
                        related_name="partitions",
                        related_query_name="partition",
                        to="slurm.slurmqos",
                        verbose_name="QOS list",
                    ),
                ),
            ],
            options={
                "verbose_name": "slurm partition",
                "verbose_name_plural": "slurm partitions",
                "ordering": ["cluster__name", "name"],
                "constraints": [
                    models.UniqueConstraint(fields=("cluster", "name"), name="slurm_slurmpartition_unique_cluster_name")
                ],
            },
            bases=(coldfront.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name="slurmaccount",
            constraint=models.UniqueConstraint(
                fields=("cluster", "name"), name="slurm_slurmaccount_unique_cluster_name"
            ),
        ),
        migrations.AddConstraint(
            model_name="slurmuser",
            constraint=models.UniqueConstraint(fields=("user", "cluster"), name="slurm_slurmuser_unique_user_cluster"),
        ),
    ]
