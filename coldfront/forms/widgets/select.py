# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django import forms


class HTMXSelect(forms.Select):
    """
    Selection widget that will re-generate the HTML form upon the selection of a new option.
    """

    def __init__(self, method="get", hx_url=".", hx_target_id="form_fields", attrs=None, **kwargs):
        method = method.lower()
        if method not in ("delete", "get", "patch", "post", "put"):
            raise ValueError(f"Unsupported HTTP method: {method}")
        _attrs = {
            f"hx-{method}": hx_url,
            "hx-include": f"#{hx_target_id}",
            "hx-params": "not csrfmiddlewaretoken",
            "hx-target": f"#{hx_target_id}",
        }
        if attrs:
            _attrs.update(attrs)

        super().__init__(attrs=_attrs, **kwargs)
