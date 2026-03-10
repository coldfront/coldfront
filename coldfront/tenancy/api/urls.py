# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from coldfront.api.routers import ColdFrontRouter

from . import views

router = ColdFrontRouter()
router.APIRootView = views.TenancyRootView

# Tenants
router.register("tenant-groups", views.TenantGroupViewSet)
router.register("tenants", views.TenantViewSet)

app_name = "tenancy-api"
urlpatterns = router.urls
