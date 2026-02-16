# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "coldfront.core"

    def ready(self):
        from coldfront.core import signals  # noqa: F401
        from coldfront.registry import register_models

        # Register models
        register_models(*self.get_models())
