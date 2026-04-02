# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

from coldfront.users.models import Group


class ColdFrontAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.
        """
        return True

    def get_user_signed_up_signal(self):
        return user_signed_up


class ColdFrontSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        username = sociallogin.user.username
        if not sociallogin.is_existing and username:
            try:
                user = get_user_model().objects.get(username=username)
                sociallogin.connect(request, user)
            except get_user_model().DoesNotExist:
                pass

        self._sync_groups(sociallogin.user, sociallogin.account.extra_data)

    def _sync_groups(self, user, claims):
        groups = claims.get("groups", [])
        if not groups:
            userinfo = claims.get("userinfo", {})
            groups = userinfo.get("groups", [])

        if user.pk:
            for group_name in groups:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
