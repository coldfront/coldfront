# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from .models import Group, User


class ColdFrontUserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
    search_fields = ["username"]


class ColdFrontGroupAdmin(GroupAdmin):
    model = Group
    list_display = ["name", "description"]
    search_fields = ["name"]


admin.site.register(User, ColdFrontUserAdmin)
admin.site.register(Group, ColdFrontGroupAdmin)
