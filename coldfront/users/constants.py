# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import string

from django.db.models import Q

OBJECTPERMISSION_OBJECT_TYPES = (Q(public=True) & ~Q(app_label="core", model="objecttype")) | Q(
    app_label="core", model__in=["taggeditem"]
)

CONSTRAINT_TOKEN_USER = "$user"

# API tokens
TOKEN_PREFIX = "cft_"
TOKEN_KEY_LENGTH = 12
TOKEN_DEFAULT_LENGTH = 40
TOKEN_CHARSET = string.ascii_letters + string.digits
