# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from shortuuid import ShortUUID


def auto_generate_slug(model_instance=None):
    """Auto generate a slug. This is the default implementation which generates a shortuuid of length 7 form a numeric alphabet"""

    from coldfront.ras.models import Allocation, Project

    prefix = "cf-"

    if model_instance is not None:
        if issubclass(model_instance.__class__, Project):
            prefix = "proj-"
        elif issubclass(model_instance.__class__, Allocation):
            prefix = "alloc-"

    return prefix + ShortUUID(alphabet="0123456789").random(length=7)
