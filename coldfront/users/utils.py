# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings

__all__ = ("get_current_pepper",)


def get_current_pepper():
    """
    Return the ID and value of the newest (highest ID) cryptographic pepper.
    """
    if not settings.API_TOKEN_PEPPERS:
        raise ValueError("API_TOKEN_PEPPERS is not defined")
    newest_id = sorted(settings.API_TOKEN_PEPPERS.keys())[-1]
    return newest_id, settings.API_TOKEN_PEPPERS[newest_id]
