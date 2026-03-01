# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import include, path

from coldfront.registry import get_model_urls

from . import views  # noqa F401

app_name = "users"
urlpatterns = [
    path("users/", include(get_model_urls("users", "user", detail=False))),
    path("users/<int:pk>/", include(get_model_urls("users", "user"))),
    path("groups/", include(get_model_urls("users", "group", detail=False))),
    path("groups/<int:pk>/", include(get_model_urls("users", "group"))),
    path("permissions/", include(get_model_urls("users", "objectpermission", detail=False))),
    path("permissions/<int:pk>/", include(get_model_urls("users", "objectpermission"))),
]
