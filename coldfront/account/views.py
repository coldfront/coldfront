# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from coldfront.account.models import UserToken
from coldfront.core.models import ObjectChange
from coldfront.core.tables import ObjectChangeTable
from coldfront.registry import register_model_view
from coldfront.users import forms
from coldfront.views import generic

from .forms import PasswordChangeForm
from .tables import UserTokenTable

#
# Login/logout
#


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


#
# User profiles
#


class ProfileView(LoginRequiredMixin, View):
    template_name = "account/profile.html"

    def get(self, request):

        # Compile changelog table
        changelog = ObjectChange.objects.valid_models().restrict(request.user, "view").filter(user=request.user)[:20]
        changelog_table = ObjectChangeTable(changelog)
        changelog_table.orderable = False
        changelog_table.configure(request)

        return render(
            request,
            self.template_name,
            {
                "changelog_table": changelog_table,
                "active_tab": "profile",
            },
        )


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = "account/password.html"

    def get(self, request):
        # LDAP users cannot change their password here
        if getattr(request.user, "ldap_username", None):
            messages.warning(request, _("LDAP-authenticated user credentials cannot be changed within ColdFront."))
            return redirect("account:profile")

        form = PasswordChangeForm(user=request.user)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "active_tab": "password",
            },
        )

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, _("Your password has been changed successfully."))
            return redirect("account:profile")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "active_tab": "change_password",
            },
        )


#
# User views for token management
#


@register_model_view(UserToken, "list", path="", detail=False)
class UserTokenListView(generic.ObjectListView):
    template_name = "account/usertoken_list.html"
    table = UserTokenTable

    def get_queryset(self, request):
        return UserToken.objects.filter(user=request.user)

    def get_extra_context(self, request):
        return {
            "active_tab": "api-tokens",
        }


@register_model_view(UserToken)
class UserTokenView(generic.ObjectView):
    def get_queryset(self, request):
        return UserToken.objects.filter(user=request.user)


@register_model_view(UserToken, "add", detail=False)
@register_model_view(UserToken, "edit")
class UserTokenEditView(generic.ObjectEditView):
    form = forms.UserTokenForm
    default_return_url = "account:usertoken_list"

    def get_queryset(self, request):
        return UserToken.objects.filter(user=request.user)

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            obj.user = request.user
        return obj


@register_model_view(UserToken, "delete")
class UserTokenDeleteView(generic.ObjectDeleteView):
    default_return_url = "account:usertoken_list"

    def get_queryset(self, request):
        return UserToken.objects.filter(user=request.user)
