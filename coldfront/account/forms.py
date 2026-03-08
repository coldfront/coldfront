# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from crispy_forms.layout import Layout
from django.contrib.auth.forms import PasswordChangeForm as _PasswordChangeForm

from coldfront.forms.mixins import HorizontalFormMixin


class PasswordChangeForm(HorizontalFormMixin, _PasswordChangeForm):
    fieldsets = (
        Layout(
            "old_password",
            "new_password1",
            "new_password2",
        ),
    )
