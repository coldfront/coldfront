# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

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
