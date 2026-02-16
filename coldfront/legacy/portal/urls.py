# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import path

import coldfront.legacy.portal.views as portal_views

urlpatterns = [
    path(
        "data/allocation-by-status/",
        portal_views.allocation_by_status,
        name="portal-allocation-status",
    ),
    path(
        "data/resource-by-type/",
        portal_views.resource_by_type,
        name="portal-resource-type",
    ),
]
