# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.apps import AppConfig


class RASConfig(AppConfig):
    name = "coldfront.ras"
    verbose_name = "RAS"

    def ready(self):
        from coldfront.models.features import register_models

        register_models(*self.get_models())
