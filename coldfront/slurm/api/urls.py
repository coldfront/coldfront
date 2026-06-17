# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.api.routers import ColdFrontRouter

from . import views

router = ColdFrontRouter()
router.APIRootView = views.SlurmRootView

# Clusters
router.register("clusters", views.SlurmClusterViewSet)

# Partitions
router.register("partitions", views.SlurmPartitionViewSet)

app_name = "slurm-api"
urlpatterns = router.urls
