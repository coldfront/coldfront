# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path

from coldfront.registry import get_model_urls

from . import views  # noqa F401

app_name = "slurm"
urlpatterns = [
    path("clusters/", include(get_model_urls("slurm", "slurmcluster", detail=False))),
    path("clusters/<int:pk>/", include(get_model_urls("slurm", "slurmcluster"))),
    path("partitions/", include(get_model_urls("slurm", "slurmpartition", detail=False))),
    path("partitions/<int:pk>/", include(get_model_urls("slurm", "slurmpartition"))),
]
