# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.models import OrganizationalModel, PrimaryModel
from coldfront.models.features import AttributeProfileMixin, CustomAttributesMixin
from coldfront.ras.choices import AllocationStatusChoices


class AllocationType(AttributeProfileMixin, OrganizationalModel):
    """
    An AllocationType defines the attributes which can be set on one or more Allocations.
    """

    clone_fields = ("schema",)

    class Meta:
        ordering = ["name"]
        verbose_name = _("allocation type")
        verbose_name_plural = _("allocation types")


class Allocation(CustomAttributesMixin, PrimaryModel):
    """
    An Allocation provides users access to resources.
    """

    allocation_type = models.ForeignKey(
        to="ras.AllocationType",
        on_delete=models.PROTECT,
        related_name="allocations",
        blank=True,
        null=True,
    )

    project = models.ForeignKey(
        to="ras.Project",
        on_delete=models.PROTECT,
        related_name="allocations",
    )

    resources = models.ManyToManyField(
        to="ras.Resource",
        related_name="allocations",
        help_text=_("The resources for this allocation"),
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="allocations",
        on_delete=models.PROTECT,
        null=False,
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=50,
        choices=AllocationStatusChoices,
        default=AllocationStatusChoices.STATUS_NEW,
    )

    start_date = models.DateTimeField(
        verbose_name=_("start date"),
        blank=True,
        null=True,
    )

    end_date = models.DateTimeField(
        verbose_name=_("end date"),
        blank=True,
        null=True,
    )

    justification = models.TextField(
        verbose_name=_("justification"),
        blank=True,
        null=True,
    )

    description = models.CharField(
        verbose_name=_("description"),
        max_length=200,
        blank=True,
        null=True,
    )

    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="allocations",
        blank=True,
        null=True,
    )

    clone_fields = (
        "description",
        "status",
    )

    prerequisite_models = (
        "ras.Project",
        "ras.Resource",
        "ras.AllocationType",
    )

    profile_field_name = "allocation_type"

    class Meta:
        ordering = ["start_date"]
        verbose_name = _("allocation")
        verbose_name_plural = _("allocations")

    def get_status_color(self):
        return AllocationStatusChoices.colors.get(self.status)

    def __str__(self):
        return f"Allocation-{self.id}"
