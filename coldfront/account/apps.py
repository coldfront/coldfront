# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "coldfront.account"
    label = "coldfront_account"

    def ready(self):
        from coldfront.models.features import register_models

        # Register models
        register_models(*self.get_models())
