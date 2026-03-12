# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0

from django import forms
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from coldfront.core.choices import ColorChoices
from coldfront.utils.forms import add_blank_choice
from coldfront.utils.validators import ColorValidator


class ColorField(models.CharField):
    default_validators = [ColorValidator]
    description = "A hexadecimal RGB color code"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = forms.Select(
            choices=add_blank_choice(ColorChoices),
            attrs={"class": "color-select"},
        )
        kwargs["help_text"] = format_html(_("RGB color in hexadecimal. Example: ") + "<code>00ff00</code>")
        return super().formfield(**kwargs)
