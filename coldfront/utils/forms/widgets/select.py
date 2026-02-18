# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django import forms

from coldfront.core.choices import ColorChoices
from coldfront.utils.forms import add_blank_choice


class ColorSelect(forms.Select):
    """
    Extends the built-in Select widget to colorize each <option>.
    """

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = add_blank_choice(ColorChoices)
        super().__init__(*args, **kwargs)
        self.attrs["class"] = "color-select"
