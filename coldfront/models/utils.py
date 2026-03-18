# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from shortuuid import ShortUUID


def auto_generate_slug(model_instance=None):
    """Auto generate a slug. This is the default implementation which generates a shortuuid of length 7"""
    return settings.AUTO_SLUG_PREFIX + ShortUUID().random(length=7)
