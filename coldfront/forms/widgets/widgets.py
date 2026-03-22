# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django import forms


class MarkdownWidget(forms.Textarea):
    """
    Provide a live preview for Markdown-formatted content.
    """

    template_name = "widgets/markdown_input.html"

    def __init__(self, attrs=None):
        # Markdown fields should use monospace font
        default_attrs = {
            "class": "font-monospace",
        }
        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)
