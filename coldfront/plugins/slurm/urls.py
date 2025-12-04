# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import path

from coldfront.plugins.slurm.views import get_full_slurm_help, get_slurm_help

urlpatterns = [
    path("full-slurm-help/", get_full_slurm_help, name="full-slurm-help"),
    path("slurm-help/", get_slurm_help, name="slurm-help"),
]
