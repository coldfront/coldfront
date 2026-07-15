# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from coldfront.models import OrganizationalModel, PrimaryModel
from coldfront.models.features import AllocatableResourceMixin


class SlurmQOS(OrganizationalModel):
    """
    A model representing a Slurm Quality of Service profile.
    Referenced by SlurmPartition.qos_list (M2M), SlurmCluster.qos_list (M2M),
    and SlurmAccount.qos_list (M2M).
    """

    class Meta:
        ordering = ["name"]
        verbose_name = _("slurm qos")
        verbose_name_plural = _("slurm qos")

    def get_status_color(self):
        return "green"


class SlurmCluster(AllocatableResourceMixin, PrimaryModel):
    """
    A Slurm cluster represents a compute cluster managed by the Slurm workload
    manager. It tracks the cluster name, its partitions, and custom attributes
    needed for generating Slurm association files or REST API calls.
    """

    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="slurm_clusters",
        blank=True,
        null=True,
    )

    default_qos = models.ForeignKey(
        to="slurm.SlurmQOS",
        on_delete=models.PROTECT,
        related_name="default_for_clusters",
        blank=True,
        null=True,
        verbose_name=_("default QOS"),
    )

    qos_list = models.ManyToManyField(
        to="slurm.SlurmQOS",
        blank=True,
        related_name="clusters",
        related_query_name="cluster",
        verbose_name=_("QOS list"),
    )

    fairshare = models.PositiveIntegerField(
        blank=True,
        default=1,
        verbose_name=_("fairshare"),
    )

    features = models.JSONField(
        blank=True,
        null=True,
        default=list,
        verbose_name=_("features"),
    )

    classification = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("classification"),
    )

    clone_fields = (
        "locked",
        "tenant",
        "default_qos",
        "qos_list",
        "fairshare",
        "features",
        "classification",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("slurm cluster")
        verbose_name_plural = _("slurm clusters")

    def __str__(self):
        return self.name

    def get_status_color(self):
        return "green"


class SlurmPartition(AllocatableResourceMixin, PrimaryModel):
    """
    A Slurm partition belongs to a SlurmCluster and represents a job
    submission queue within the cluster. Partitions have resource limits,
    node allocations, and scheduling policies that are needed for generating
    Slurm association data.
    """

    cluster = models.ForeignKey(
        to="slurm.SlurmCluster",
        on_delete=models.PROTECT,
        related_name="partitions",
        verbose_name=_("cluster"),
    )

    max_jobs = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("max jobs"),
    )

    max_submit_jobs = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("max submit jobs"),
    )

    max_tres_per_job = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("max TRES per job"),
    )

    max_tres_per_node = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("max TRES per node"),
    )

    max_tres_mins_per_job = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("max TRES minutes per job"),
    )

    max_wall_duration_per_job = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_("max wall duration per job"),
    )

    fairshare = models.PositiveIntegerField(
        blank=True,
        default=1,
        verbose_name=_("fairshare"),
    )

    qos_list = models.ManyToManyField(
        to="slurm.SlurmQOS",
        blank=True,
        related_name="partitions",
        related_query_name="partition",
        verbose_name=_("QOS list"),
    )

    allow_groups = models.ManyToManyField(
        to="users.Group",
        blank=True,
        related_name="allowed_partitions",
        related_query_name="allowed_partition",
        verbose_name=_("allowed groups"),
    )

    allow_accounts = models.ManyToManyField(
        to="slurm.SlurmAccount",
        blank=True,
        related_name="allowed_partitions",
        related_query_name="allowed_partition",
        verbose_name=_("allowed accounts"),
    )

    nodes = models.TextField(
        blank=True,
        default="",
        verbose_name=_("nodes"),
        help_text=_("Comma-separated node list for this partition (e.g., node[01-64])."),
    )

    priority = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("priority"),
    )

    is_default = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_("default"),
    )

    default_time = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_("default time"),
    )

    state = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("state"),
    )

    preempt_mode = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("preempt mode"),
    )

    def_mem_per_cpu = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("default memory per CPU"),
    )

    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=100,
        blank=True,
        unique=True,
    )

    clone_fields = (
        "cluster",
        "locked",
        "max_jobs",
        "max_submit_jobs",
        "max_tres_per_job",
        "max_tres_per_node",
        "max_tres_mins_per_job",
        "max_wall_duration_per_job",
        "fairshare",
        "qos_list",
        "allow_groups",
        "allow_accounts",
        "nodes",
        "priority",
        "is_default",
        "default_time",
        "state",
        "preempt_mode",
        "def_mem_per_cpu",
        "slug",
    )

    prerequisite_models = ("slurm.SlurmCluster",)

    class Meta:
        ordering = ["cluster__name", "name"]
        verbose_name = _("slurm partition")
        verbose_name_plural = _("slurm partitions")
        constraints = (
            models.UniqueConstraint(
                fields=("cluster", "name"),
                name="%(app_label)s_%(class)s_unique_cluster_name",
            ),
        )

    def __str__(self):
        return f"{self.name} ({self.cluster.name})"

    def get_status_color(self):
        return "green"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.cluster.name}-{self.name}")
        super().save(*args, **kwargs)


class SlurmAccount(PrimaryModel):
    """
    A named Slurm accounting account, matching Slurm's acct_table.
    Accounts are lean containers (name, description, organization) --
    all per-association limits live on SlurmAssociation instead.
    """

    name = models.CharField(
        verbose_name=_("name"),
        max_length=100,
    )

    cluster = models.ForeignKey(
        to="slurm.SlurmCluster",
        on_delete=models.PROTECT,
        related_name="accounts",
        verbose_name=_("cluster"),
    )

    fairshare = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=None,
        verbose_name=_("fairshare"),
    )

    qos_list = models.ManyToManyField(
        to="slurm.SlurmQOS",
        blank=True,
        related_name="accounts",
        related_query_name="account",
        verbose_name=_("QOS list"),
    )

    clone_fields = (
        "cluster",
        "fairshare",
        "qos_list",
    )

    prerequisite_models = ("slurm.SlurmCluster",)

    class Meta:
        ordering = ["cluster__name", "name"]
        verbose_name = _("slurm account")
        verbose_name_plural = _("slurm accounts")
        constraints = (
            models.UniqueConstraint(
                fields=("cluster", "name"),
                name="%(app_label)s_%(class)s_unique_cluster_name",
            ),
        )

    def __str__(self):
        return f"{self.name} ({self.cluster.name})"

    def get_status_color(self):
        return "green"


class SlurmAssociation(PrimaryModel):
    """
    Bridges an Allocation to its SlurmAccount, carrying all per-association
    limits. This matches Slurm's assoc_table where each (cluster, account,
    user, partition) row carries its own limits, fairshare, and hierarchy.
    Created when an allocation is requested (via ViewFlow callback), and the
    SlurmAccount is set later by an admin or automated process before the
    allocation is approved.
    """

    allocation = models.ForeignKey(
        to="ras.Allocation",
        on_delete=models.PROTECT,
        related_name="slurm_associations",
        unique=True,
        verbose_name=_("allocation"),
    )

    slurm_account = models.ForeignKey(
        to="slurm.SlurmAccount",
        on_delete=models.PROTECT,
        related_name="associations",
        blank=True,
        null=True,
        verbose_name=_("Slurm account"),
    )

    parent = models.ForeignKey(
        to="slurm.SlurmAccount",
        on_delete=models.PROTECT,
        related_name="child_associations",
        blank=True,
        null=True,
        verbose_name=_("parent account"),
    )

    default_qos = models.ForeignKey(
        to="slurm.SlurmQOS",
        on_delete=models.PROTECT,
        related_name="associations",
        blank=True,
        null=True,
        verbose_name=_("default QOS"),
    )

    fairshare = models.PositiveIntegerField(
        blank=True,
        default=1,
        verbose_name=_("fairshare"),
    )

    max_jobs = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("max jobs"),
    )

    max_submit_jobs = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("max submit jobs"),
    )

    max_tres_per_job = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("max TRES per job"),
    )

    max_tres_mins_per_job = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("max TRES minutes per job"),
    )

    max_wall_duration_per_job = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_("max wall duration per job"),
    )

    def clean(self):
        """
        Validate that the slurm_account does not create duplicate
        (user, acct, partition) tuples in the Slurm dump.

        Raises ValidationError if another SlurmAssociation with the same
        slurm_account targets the same resource scope:
          - Same SlurmCluster directly (partition='')
          - Same SlurmPartition (partition='<name>')
        """
        super().clean()
        if self.slurm_account is None:
            return

        allocation = self.allocation
        if allocation is None:
            return
        resource = allocation.resource_object
        if resource is None:
            return

        # Query other associations with the same slurm_account, excluding self
        qs = SlurmAssociation.objects.filter(slurm_account=self.slurm_account)
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if isinstance(resource, SlurmCluster):
            # Direct-to-cluster: check no other association targets the same
            # cluster directly with the same account
            cluster_ct = ContentType.objects.get_for_model(SlurmCluster)
            for other in qs.select_related("allocation"):
                other_alloc = other.allocation
                if (
                    other_alloc.resource_object_type_id == cluster_ct.pk
                    and other_alloc.resource_object_id == resource.pk
                ):
                    raise ValidationError(
                        _(
                            "Another association already uses account "
                            "'%(account)s' for a direct allocation on "
                            "cluster '%(cluster)s'."
                        )
                        % {
                            "account": self.slurm_account.name,
                            "cluster": resource.name,
                        }
                    )

        elif isinstance(resource, SlurmPartition):
            # Partition-specific: check no other association targets the same
            # partition with the same account
            partition_ct = ContentType.objects.get_for_model(SlurmPartition)
            for other in qs.select_related("allocation"):
                other_alloc = other.allocation
                if (
                    other_alloc.resource_object_type_id == partition_ct.pk
                    and other_alloc.resource_object_id == resource.pk
                ):
                    raise ValidationError(
                        _(
                            "Another association already uses account "
                            "'%(account)s' for partition '%(partition)s' "
                            "on cluster '%(cluster)s'."
                        )
                        % {
                            "account": self.slurm_account.name,
                            "partition": resource.name,
                            "cluster": resource.cluster.name,
                        }
                    )

    clone_fields = (
        "slurm_account",
        "parent",
        "default_qos",
        "fairshare",
        "max_jobs",
        "max_submit_jobs",
        "max_tres_per_job",
        "max_tres_mins_per_job",
        "max_wall_duration_per_job",
    )

    prerequisite_models = ("ras.Allocation",)

    class Meta:
        ordering = ["allocation__slug"]
        verbose_name = _("slurm association")
        verbose_name_plural = _("slurm associations")

    def __str__(self):
        acct = self.slurm_account
        return f"Association {acct.name if acct else '?'} -> {self.allocation}"

    def get_status_color(self):
        return "green"


class SlurmUser(PrimaryModel):
    """
    Tracks each user's default account per cluster, matching Slurm's
    slurmdb_user_rec_t. This cleanly separates the default account concept
    from individual SlurmAssociation records.
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="slurm_users",
        verbose_name=_("user"),
    )

    cluster = models.ForeignKey(
        to="slurm.SlurmCluster",
        on_delete=models.PROTECT,
        related_name="users",
        verbose_name=_("cluster"),
    )

    default_account = models.ForeignKey(
        to="slurm.SlurmAccount",
        on_delete=models.PROTECT,
        related_name="default_for_users",
        verbose_name=_("default account"),
    )

    default_wckey = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("default wckey"),
    )

    default_qos = models.ForeignKey(
        to="slurm.SlurmQOS",
        on_delete=models.PROTECT,
        related_name="default_for_users",
        blank=True,
        null=True,
        verbose_name=_("default QOS"),
    )

    admin_level = models.SmallIntegerField(
        choices=[
            (0, _("None")),
            (1, _("Operator")),
            (2, _("Admin")),
        ],
        blank=True,
        null=True,
        verbose_name=_("admin level"),
    )

    clone_fields = (
        "cluster",
        "default_account",
        "default_wckey",
        "default_qos",
    )

    prerequisite_models = (
        "slurm.SlurmCluster",
        "slurm.SlurmAccount",
    )

    class Meta:
        ordering = ["cluster__name", "user__username"]
        verbose_name = _("slurm user")
        verbose_name_plural = _("slurm users")
        constraints = (
            models.UniqueConstraint(
                fields=("user", "cluster"),
                name="%(app_label)s_%(class)s_unique_user_cluster",
            ),
        )

    def __str__(self):
        return f"{self.user.username} ({self.cluster.name})"

    def get_status_color(self):
        return "green"
