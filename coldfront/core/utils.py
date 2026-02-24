# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import decimal

from django.core.serializers.json import DjangoJSONEncoder
from taggit.managers import _TaggableManager


class CustomFieldJSONEncoder(DjangoJSONEncoder):
    """
    Override Django's built-in JSON encoder to save decimal values as JSON numbers.
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


def is_taggable(obj):
    """
    Return True if the instance can have Tags assigned to it; False otherwise.
    """
    if hasattr(obj, "tags"):
        if issubclass(obj.tags.__class__, _TaggableManager):
            return True
    return False
