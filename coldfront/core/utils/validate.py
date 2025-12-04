# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime

from django.core.exceptions import ValidationError
from formencode import validators


class AttributeValidator:
    def __init__(self, value):
        self.value = value

    def _raise_if_empty(self):
        if self.value == "":
            raise ValidationError(f'Invalid Value "{self.value}". Value cannot be empty.')

    def validate_int(self):
        self._raise_if_empty()
        try:
            validate = validators.Int()
            validate.to_python(self.value)
        except Exception:
            raise ValidationError(f"Invalid Value {self.value}. Value must be an int.")

    def validate_float(self):
        self._raise_if_empty()
        try:
            validate = validators.Number()
            validate.to_python(self.value)
        except Exception:
            raise ValidationError(f"Invalid Value {self.value}. Value must be an float.")

    def validate_yes_no(self):
        self._raise_if_empty()
        try:
            validate = validators.OneOf(["Yes", "No"])
            validate.to_python(self.value)
        except Exception:
            raise ValidationError(f"Invalid Value {self.value}. Value must be an Yes/No value.")

    def validate_date(self):
        try:
            datetime.datetime.strptime(self.value.strip(), "%Y-%m-%d")
        except Exception:
            raise ValidationError(
                f"Invalid Value {self.value}. Date must be in format YYYY-MM-DD and date must be today or later."
            )
