# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from rest_framework import routers

from .views import DummyViewSet

router = routers.DefaultRouter()
router.register("dummy-models", DummyViewSet)
urlpatterns = router.urls
