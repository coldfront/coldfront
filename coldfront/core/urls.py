# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import include, path

from coldfront.registry import get_model_urls

from . import views

app_name = "core"
urlpatterns = [
    path("tags/", include(get_model_urls("core", "tag", detail=False))),
    path("tags/<int:pk>/", include(get_model_urls("core", "tag"))),
    path("changelog/", include(get_model_urls("core", "objectchange", detail=False))),
    path("changelog/<int:pk>/", include(get_model_urls("core", "objectchange"))),
    path("custom-field-choices/", include(get_model_urls("core", "customfieldchoiceset", detail=False))),
    path("custom-field-choices/<int:pk>/", include(get_model_urls("core", "customfieldchoiceset"))),
    path("custom-fields/", include(get_model_urls("core", "customfield", detail=False))),
    path("custom-fields/<int:pk>/", include(get_model_urls("core", "customfield"))),
    path("plugins/", views.PluginListView.as_view(), name="plugin_list"),
    path("plugins/<str:name>/", views.PluginView.as_view(), name="plugin"),
]
