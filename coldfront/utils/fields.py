# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from coldfront.utils.forms.widgets import ColorSelect
from coldfront.utils.validators import ColorValidator

__all__ = ("ColorField",)


class ColorField(models.CharField):
    default_validators = [ColorValidator]
    description = "A hexadecimal RGB color code"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = ColorSelect
        kwargs["help_text"] = format_html(_("RGB color in hexadecimal. Example: ") + "<code>00ff00</code>")
        return super().formfield(**kwargs)


class CounterCacheField(models.BigIntegerField):
    """
    Counter field to keep track of related model counts.
    """

    def __init__(self, to_model, to_field, *args, **kwargs):
        if not isinstance(to_model, str):
            raise TypeError(
                _(
                    "%s(%r) is invalid. to_model parameter to CounterCacheField must be "
                    "a string in the format 'app.model'"
                )
                % (
                    self.__class__.__name__,
                    to_model,
                )
            )

        if not isinstance(to_field, str):
            raise TypeError(
                _("%s(%r) is invalid. to_field parameter to CounterCacheField must be a string in the format 'field'")
                % (
                    self.__class__.__name__,
                    to_field,
                )
            )

        self.to_model_name = to_model
        self.to_field_name = to_field

        kwargs["default"] = kwargs.get("default", 0)
        kwargs["editable"] = False

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["to_model"] = self.to_model_name
        kwargs["to_field"] = self.to_field_name
        return name, path, args, kwargs
