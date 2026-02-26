# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import jsonschema
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonschema.exceptions import ValidationError as JSONValidationError

from coldfront.models import OrganizationalModel, PrimaryModel
from coldfront.ras.choices import AllocationStatusChoices
from coldfront.utils.jsonschema import validate_schema
from coldfront.utils.strings import title


class AllocationType(OrganizationalModel):
    """
    An AllocationType defines the attributes which can be set on one or more Allocations.
    """

    schema = models.JSONField(
        blank=True,
        null=True,
        validators=[validate_schema],
        verbose_name=_("schema"),
    )

    clone_fields = ("schema",)

    class Meta:
        verbose_name = _("allocation type")
        verbose_name_plural = _("allocation types")


class Allocation(PrimaryModel):
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

    attribute_data = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("attributes"),
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

    class Meta:
        verbose_name = _("allocation")
        verbose_name_plural = _("allocations")

    def get_status_color(self):
        return AllocationStatusChoices.colors.get(self.status)

    @property
    def attributes(self):
        """
        Returns a human-friendly representation of the attributes defined for an Allocation according to its type.
        """
        if not self.attribute_data or self.allocation_type is None or not self.allocation_type.schema:
            return {}
        attrs = {}
        for name, options in self.allocation_type.schema.get("properties", {}).items():
            key = options.get("title", title(name))
            attrs[key] = self.attribute_data.get(name)
        return dict(sorted(attrs.items()))

    def clean(self):
        super().clean()

        # Validate any attributes against the assigned allocation type's schema
        if self.allocation_type and self.allocation_type.schema:
            try:
                jsonschema.validate(self.attribute_data, schema=self.allocation_type.schema)
            except JSONValidationError as e:
                raise ValidationError(_("Invalid schema: {error}").format(error=e))
        else:
            self.attribute_data = None

    def __str__(self):
        return f"Allocation-{self.id}"
