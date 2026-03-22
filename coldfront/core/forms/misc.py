# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django import forms
from django.utils.translation import gettext_lazy as _


class RenderMarkdownForm(forms.Form):
    """
    Provides basic validation for markup to be rendered.
    """

    text = forms.CharField(label=_("Text"), required=False)
