# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.models import ColdFrontModel, PrimaryModel
from coldfront.models.features import CustomAttributesMixin
from coldfront.models.fields import AutoSlugField
from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.flows import AllocationStatusFlow


class Allocation(CustomAttributesMixin, PrimaryModel):
    """
    An Allocation provides users access to resources.
    """

    slug = AutoSlugField(
        verbose_name=_("slug"),
    )
    project = models.ForeignKey(
        to="ras.Project",
        on_delete=models.PROTECT,
        related_name="allocations",
    )
    resource = models.ForeignKey(
        to="ras.Resource",
        on_delete=models.PROTECT,
        related_name="allocations",
        help_text=_("The resource for this allocation"),
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="owned_allocations",
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
    comments = models.TextField(
        verbose_name=_("comments"),
        blank=True,
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
    )

    profile_field_name = "resource"

    class Meta:
        ordering = ["start_date"]
        verbose_name = _("allocation")
        verbose_name_plural = _("allocations")

    def _get_schema(self, profile):
        if profile and profile.resource_type:
            return profile.resource_type.allocation_schema

    def get_status_color(self):
        return AllocationStatusChoices.colors.get(self.status)

    def get_outgoing_transitions(self):
        if not self.status:
            return []

        return [t.slug for t in AllocationStatusFlow.status.get_outgoing_transitions(self.status)]

    def __str__(self):
        return f"Allocation {self.slug}"


class AllocationUser(ColdFrontModel):
    """A user that is a member of an allocation"""

    allocation = models.ForeignKey(
        to="ras.Allocation",
        on_delete=models.PROTECT,
        related_name="users",
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="allocations",
        on_delete=models.PROTECT,
        null=False,
    )

    clone_fields = ("allocation",)

    prerequisite_models = ("ras.Allocation",)

    class Meta:
        ordering = ["id"]
        unique_together = ("user", "allocation")
        verbose_name = _("allocation user")
        verbose_name_plural = _("allocation users")

    def __str__(self):
        return self.user.username
