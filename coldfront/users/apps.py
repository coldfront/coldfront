# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "coldfront.users"

    def ready(self):
        from coldfront.models.features import register_models

        # Register models
        register_models(*self.get_models())
