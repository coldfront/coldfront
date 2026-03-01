# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.db.models import Q

OBJECTPERMISSION_OBJECT_TYPES = (Q(public=True) & ~Q(app_label="core", model="objecttype")) | Q(
    app_label="core", model__in=["taggeditem"]
)

CONSTRAINT_TOKEN_USER = "$user"
