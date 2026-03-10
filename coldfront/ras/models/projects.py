# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.models import OrganizationalModel
from coldfront.ras.choices import ProjectStatusChoices


class Project(OrganizationalModel):
    """A project is a container for housing research summary information related to allocation requests"""

    status = models.CharField(
        verbose_name=_("status"),
        max_length=50,
        choices=ProjectStatusChoices,
        default=ProjectStatusChoices.STATUS_NEW,
    )

    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="projects",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="projects",
        on_delete=models.PROTECT,
        null=False,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def get_status_color(self):
        return ProjectStatusChoices.colors.get(self.status)
