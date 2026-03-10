# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0


from collections import defaultdict
from contextlib import contextmanager

from django.conf import settings as django_settings

from coldfront.context import current_request, query_cache, signals_received
from coldfront.registry import register_request_processor
from coldfront.registry import registry as registry_

__all__ = (
    "registry",
    "settings",
)


@register_request_processor
@contextmanager
def event_tracking(request):
    """
    Queue interesting events in memory while processing a request, then flush that queue for processing by the
    events pipline before returning the response.

    :param request: WSGIRequest object with a unique `id` set
    """
    current_request.set(request)
    query_cache.set(defaultdict(dict))
    signals_received.set(defaultdict(dict))

    yield

    # Clear context vars
    current_request.set(None)
    query_cache.set(None)
    signals_received.set(None)


def registry(request):
    """
    Adds ColdFront registry items to the template context. Example: {{ registry.models.core }}
    """
    return {
        "registry": registry_,
    }


def settings(request):
    """
    Adds Django settings to the template context. Example: {{ settings.DEBUG }}
    """
    return {
        "settings": django_settings,
    }
