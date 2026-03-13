# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.models import ColdFrontModel, OrganizationalModel
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
        related_name="owned_projects",
        on_delete=models.PROTECT,
        null=False,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def get_status_color(self):
        return ProjectStatusChoices.colors.get(self.status)


class ProjectUser(ColdFrontModel):
    """A user that is a member of a project"""

    project = models.ForeignKey(
        to="ras.Project",
        on_delete=models.PROTECT,
        related_name="users",
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="projects",
        on_delete=models.PROTECT,
        null=False,
    )

    clone_fields = ("project",)

    prerequisite_models = ("ras.Project",)

    class Meta:
        ordering = ["id"]
        verbose_name = _("project user")
        verbose_name_plural = _("project users")

    def __str__(self):
        return self.user.username
