# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
ColdFront URL Configuration
"""

import environ
import split_settings
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView

from coldfront.auth.logout import HtmxLogoutView
from coldfront.config.env import ENV, PROJECT_ROOT
from coldfront.views import HomeView

admin.site.site_header = "ColdFront Administration"
admin.site.site_title = "ColdFront Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    # Base views
    path("", HomeView.as_view(), name="home"),
    # Login/logout
    path(
        "login",
        LoginView.as_view(template_name="auth/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", HtmxLogoutView.as_view(), name="logout"),
    # ColdFront core apps
    path("users/", include("coldfront.users.urls")),
    path("core/", include("coldfront.core.urls")),
    path("tenancy/", include("coldfront.tenancy.urls")),
    path("ras/", include("coldfront.ras.urls")),
]

if "mozilla_django_oidc" in settings.INSTALLED_APPS:
    urlpatterns.append(path("oidc/", include("mozilla_django_oidc.urls")))

if "django_su.backends.SuBackend" in settings.AUTHENTICATION_BACKENDS:
    urlpatterns.append(path("su/", include("django_su.urls")))


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


admin.site.add_action(export_as_json, "export_as_json")

# Local urls overrides
local_urls = [
    # Local urls relative to coldfront.config package
    "local_urls.py",
    # System wide urls for production deployments
    "/etc/coldfront/local_urls.py",
    # Local urls relative to coldfront project root
    PROJECT_ROOT("local_urls.py"),
]

if ENV.str("COLDFRONT_URLS", default="") != "":
    # Local urls from path specified via environment variable
    local_urls.append(environ.Path(ENV.str("COLDFRONT_URLS"))())

for lu in local_urls:
    split_settings.tools.include(split_settings.tools.optional(lu))
