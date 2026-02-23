# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.core.validators import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField

from coldfront.models import ChangeLoggedModel
from coldfront.models.features import CloningMixin

__all__ = ("CustomFieldChoiceSet",)


class CustomFieldChoiceSet(CloningMixin, ChangeLoggedModel):
    """
    Represents a set of choices available for choice and multi-choice custom fields.
    """

    CHOICES_SCHEMA = {
        "type": "array",
        "items": {"type": "string"},
    }

    name = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )
    choices = JSONField(
        schema=CHOICES_SCHEMA,
    )
    order_alphabetically = models.BooleanField(
        default=False,
        help_text=_("Choices are automatically ordered alphabetically"),
    )

    clone_fields = ("choices", "order_alphabetically")

    class Meta:
        ordering = ("name",)
        verbose_name = _("custom field choice set")
        verbose_name_plural = _("custom field choice sets")

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cache the initial set of choices for comparison under clean()
        self._original_choices = self.__dict__.get("choices")

    def get_absolute_url(self):
        return reverse("core:customfieldchoiceset", args=[self.pk])

    @property
    def choices_count(self):
        return len(self.choices)

    @property
    def items(self):
        """
        Returns an iterator of the choices
        """
        for c in self.choices:
            parts = c.split(":")
            if len(parts) == 1:
                yield [c, c]
            else:
                yield parts

    @property
    def values(self):
        """
        Returns an iterator of the valid choice values.
        """
        return (x.split(":")[0] for x in self.choices)

    def clean(self):
        if not self.choices:
            raise ValidationError(_("Must define a list of choices."))

        # Check for duplicate values in extra_choices
        choice_values = [c[0] for c in self.items] if self.choices else []
        if len(set(choice_values)) != len(choice_values):
            # At least one duplicate value is present. Find the first one and raise an error.
            _seen = []
            for value in choice_values:
                if value in _seen:
                    raise ValidationError(_("Duplicate value '{value}' found in choices.").format(value=value))
                _seen.append(value)

    def save(self, *args, **kwargs):

        # Sort choices if alphabetical ordering is enforced
        if self.order_alphabetically:
            self.choices = sorted(self.choices, key=lambda x: x.split(":")[0])

        return super().save(*args, **kwargs)
