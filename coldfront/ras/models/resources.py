# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.core.choices import ColorChoices
from coldfront.models import OrganizationalModel, PrimaryModel
from coldfront.models.features import AttributeProfileMixin, CustomAttributesMixin
from coldfront.ras.choices import ResourceStatusChoices
from coldfront.utils.fields import ColorField, CounterCacheField


class ResourceType(AttributeProfileMixin, OrganizationalModel):
    """
    Resources are organized by type; for example, "Cluster", "Cluster Partition", or "Storage".
    """

    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=100,
        unique=True,
    )
    color = ColorField(
        verbose_name=_("color"),
        default=ColorChoices.COLOR_GREY,
    )
    resource_count = CounterCacheField(
        to_model="ras.Resource",
        to_field="resource_type",
    )

    class Meta:
        verbose_name = _("resource type")
        verbose_name_plural = _("resource types")


class Resource(CustomAttributesMixin, PrimaryModel):
    """
    A Resource represents something that can be allocated. Each Resource is assigned a ResourceType.
    """

    name = models.CharField(
        verbose_name=_("name"),
        max_length=100,
        unique=True,
    )
    resource_type = models.ForeignKey(
        to="ras.ResourceType",
        on_delete=models.PROTECT,
        related_name="resources",
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="resources",
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=50,
        choices=ResourceStatusChoices,
        default=ResourceStatusChoices.STATUS_ACTIVE,
    )

    clone_fields = (
        "resource_type",
        "description",
        "status",
    )

    class Meta:
        verbose_name = _("resource")
        verbose_name_plural = _("resources")

    def __str__(self):
        return self.name

    def get_status_color(self):
        return ResourceStatusChoices.colors.get(self.status)

    def get_profile(self):
        return self.resource_type
