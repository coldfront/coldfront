# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse


class HtmxLogoutView(LogoutView):
    """
    LogoutView that uses htmx
    """

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            response = HttpResponse(status=204)
            response["HX-Redirect"] = redirect_to
            return response
        return super().get(request, *args, **kwargs)
