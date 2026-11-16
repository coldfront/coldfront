# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import include, path

from coldfront.core.allocation import views as allocation_views

urlpatterns = [
    path(
        "coldfront/allocation/<int:pk>/review-eula",
        allocation_views.AllocationEULAView.as_view(),
        name="allocation-review-eula",
    ),
    path("coldfront/", include("coldfront.config.urls")),
]
