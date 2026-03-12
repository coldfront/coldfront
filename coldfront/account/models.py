# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.urls import reverse

from coldfront.users.models import Token


class UserToken(Token):
    """
    Proxy model for users to manage their own API tokens.
    """

    _coldfront_private = True

    class Meta:
        proxy = True
        verbose_name = "token"

    def get_absolute_url(self):
        return reverse("account:usertoken", args=[self.pk])
