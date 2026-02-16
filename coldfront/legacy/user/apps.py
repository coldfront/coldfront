# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import importlib

from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "coldfront.legacy.user"

    def ready(self):
        importlib.import_module("coldfront.legacy.user.signals")
