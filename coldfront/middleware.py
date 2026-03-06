# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import uuid
from urllib.parse import urlparse

from .registry import apply_request_processors


class ColdFrontMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Assign a random unique ID to the request. This will be used for change logging.
        request.id = uuid.uuid4()

        # Apply all registered request processors
        with apply_request_processors(request):
            response = self.get_response(request)

        # Attach the unique request ID as an HTTP header.
        response["X-Request-ID"] = request.id

        # Enable the Vary header to help with caching of HTMX responses
        response["Vary"] = "HX-Request"

        return response


class HtmxAuthRedirectMiddleware:
    """
    Middleware to handle HTMX authentication redirects properly.

    When an HTMX request results in a 302 redirect (typically for authentication),
    this middleware:
    1. Changes the response status code to 204 (No Content)
    2. Adds an HX-Redirect header with the redirect URL
    3. Preserves the original request path in the 'next' query parameter

    This ensures that after authentication, the user is returned to the page
    they were attempting to access, maintaining a seamless UX with HTMX.

    Credits: https://www.caktusgroup.com/blog/2022/11/11/how-handle-django-login-redirects-htmx/
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # HTMX request returning 302 likely is login required.
        # Take the redirect location and send it as the HX-Redirect header value,
        # with 'next' query param set to where the request originated. Also change
        # response status code to 204 (no content) so that htmx will obey the
        # HX-Redirect header value.
        if request.headers.get("HX-Request") == "true" and response.status_code == 302:
            # Determine the next path from referer or current request path
            ref_header = request.headers.get("Referer", "")
            if ref_header:
                referer = urlparse(ref_header)
                next_path = referer.path
            else:
                next_path = request.path

            # Parse the redirect URL
            redirect_url = urlparse(response["location"])

            # Set response status code to 204 for HTMX to process the redirect
            response.status_code = 204

            # Update the "?next" query parameter
            query_params = urlparse.parse_qs(redirect_url.query)
            query_params["next"] = [next_path]
            new_query = urlparse.urlencode(query_params, doseq=True)

            # Set the new HX-Redirect header
            response.headers["HX-Redirect"] = f"{redirect_url.path}?{new_query}"

        return response
