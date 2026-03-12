# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path

from coldfront.api.routers import ColdFrontRouter

from . import views

router = ColdFrontRouter()
router.APIRootView = views.UsersRootView

router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)
router.register("tokens", views.TokenViewSet)
router.register("permissions", views.ObjectPermissionViewSet)

app_name = "users-api"
urlpatterns = [
    path("tokens/provision/", views.TokenProvisionView.as_view(), name="token_provision"),
    path("", include(router.urls)),
]
