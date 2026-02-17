# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.apps import AppConfig


class TenancyConfig(AppConfig):
    name = "coldfront.tenancy"

    def ready(self):
        from coldfront.registry import register_models

        # Register models
        register_models(*self.get_models())
