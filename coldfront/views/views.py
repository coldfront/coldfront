# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):
    template_name = "home.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {},
        )
