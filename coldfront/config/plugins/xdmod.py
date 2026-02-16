# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.config.base import INSTALLED_APPS
from coldfront.config.env import ENV

# ------------------------------------------------------------------------------
# Enable XDMoD support
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    "coldfront.legacy.plugins.xdmod",
]

XDMOD_API_URL = ENV.str("XDMOD_API_URL")
