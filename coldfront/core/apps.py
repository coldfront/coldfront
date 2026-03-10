# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "coldfront.core"

    def ready(self):
        from coldfront import context_processors  # noqa: F401
        from coldfront.models.features import register_models

        from . import (
            signals,  # noqa: F401
            views,  # noqa: F401
        )

        # Register models
        register_models(*self.get_models())
