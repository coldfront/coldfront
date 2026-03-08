# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.urls import include, path

from coldfront.registry import get_model_urls

from . import views

app_name = "account"
urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("api-tokens/", include(get_model_urls("account", "usertoken", detail=False))),
    path("api-tokens/<int:pk>/", include(get_model_urls("account", "usertoken"))),
]
