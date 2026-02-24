# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from contextvars import ContextVar

__all__ = (
    "current_request",
    "query_cache",
)


current_request = ContextVar("current_request", default=None)
query_cache = ContextVar("query_cache", default=None)
