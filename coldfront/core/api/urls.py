# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from coldfront.api.routers import ColdFrontRouter

from . import views

router = ColdFrontRouter()
router.APIRootView = views.CoreRootView

router.register("custom-fields", views.CustomFieldViewSet)
router.register("custom-field-choice-sets", views.CustomFieldChoiceSetViewSet)
router.register("tags", views.TagViewSet)
router.register("tagged-objects", views.TaggedItemViewSet)

app_name = "core-api"
urlpatterns = router.urls
