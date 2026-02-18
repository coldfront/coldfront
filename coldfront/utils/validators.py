# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0


from django.core.validators import RegexValidator

__all__ = ("ColorValidator",)


ColorValidator = RegexValidator(
    regex="^[0-9a-f]{6}$", message="Enter a valid hexadecimal RGB color code.", code="invalid"
)
