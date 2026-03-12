# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from rest_framework import routers

from .views import DummyViewSet

router = routers.DefaultRouter()
router.register("dummy-models", DummyViewSet)
urlpatterns = router.urls
