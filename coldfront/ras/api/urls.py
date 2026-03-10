# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.api.routers import ColdFrontRouter

from . import views

router = ColdFrontRouter()
router.APIRootView = views.RASRootView

# Projects
router.register("projects", views.ProjectViewSet)

# Resources
router.register("resources", views.ResourceViewSet)
router.register("resource-types", views.ResourceTypeViewSet)

# Allocations
router.register("allocations", views.AllocationViewSet)
router.register("allocation-types", views.AllocationTypeViewSet)

app_name = "ras-api"
urlpatterns = router.urls
