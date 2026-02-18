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
