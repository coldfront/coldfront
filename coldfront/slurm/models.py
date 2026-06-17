# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.models import PrimaryModel
from coldfront.models.features import AllocatableResourceMixin


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

    clone_fields = (
        "is_allocatable",
        "tenant",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Slurm cluster")
        verbose_name_plural = _("Slurm clusters")

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

    clone_fields = (
        "cluster",
        "is_allocatable",
    )

    class Meta:
        ordering = ["cluster__name", "name"]
        verbose_name = _("Slurm partition")
        verbose_name_plural = _("Slurm partitions")
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
