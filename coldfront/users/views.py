# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.db.models import Count

from coldfront.core.models import ObjectChange
from coldfront.core.tables import ObjectChangeTable
from coldfront.registry import register_model_view
from coldfront.views import generic
from coldfront.views.object_actions import AddObject, BulkExport

from . import filtersets, forms, tables
from .models import Group, ObjectPermission, Token, User

#
# Users
#


@register_model_view(User, "list", path="", detail=False)
class UserListView(generic.ObjectListView):
    queryset = User.objects.all()
    filterset = filtersets.UserFilterSet
    filterset_form = forms.UserFilterSetForm
    table = tables.UserTable


@register_model_view(User)
class UserView(generic.ObjectView):
    queryset = User.objects.all()
    template_name = "users/user.html"

    def get_extra_context(self, request, instance):
        changelog = ObjectChange.objects.valid_models().restrict(request.user, "view").filter(user=instance)[:20]
        changelog_table = ObjectChangeTable(changelog)
        changelog_table.orderable = False
        changelog_table.configure(request)

        return {
            "changelog_table": changelog_table,
        }


@register_model_view(User, "add", detail=False)
@register_model_view(User, "edit")
class UserEditView(generic.ObjectEditView):
    queryset = User.objects.all()
    form = forms.UserForm


@register_model_view(User, "delete")
class UserDeleteView(generic.ObjectDeleteView):
    queryset = User.objects.all()


#
# Groups
#


@register_model_view(Group, "list", path="", detail=False)
class GroupListView(generic.ObjectListView):
    queryset = Group.objects.annotate(users_count=Count("user")).order_by("name")
    filterset = filtersets.GroupFilterSet
    filterset_form = forms.GroupFilterSetForm
    table = tables.GroupTable


@register_model_view(Group)
class GroupView(generic.ObjectView):
    queryset = Group.objects.all()
    template_name = "users/group.html"


@register_model_view(Group, "add", detail=False)
@register_model_view(Group, "edit")
class GroupEditView(generic.ObjectEditView):
    queryset = Group.objects.all()
    form = forms.GroupForm


@register_model_view(Group, "delete")
class GroupDeleteView(generic.ObjectDeleteView):
    queryset = Group.objects.all()


#
# ObjectPermissions
#


@register_model_view(ObjectPermission, "list", path="", detail=False)
class ObjectPermissionListView(generic.ObjectListView):
    queryset = ObjectPermission.objects.all()
    filterset = filtersets.ObjectPermissionFilterSet
    filterset_form = forms.ObjectPermissionFilterSetForm
    table = tables.ObjectPermissionTable
    actions = (
        AddObject,
        BulkExport,
    )


@register_model_view(ObjectPermission)
class ObjectPermissionView(generic.ObjectView):
    queryset = ObjectPermission.objects.all()
    template_name = "users/objectpermission.html"


@register_model_view(ObjectPermission, "add", detail=False)
@register_model_view(ObjectPermission, "edit")
class ObjectPermissionEditView(generic.ObjectEditView):
    queryset = ObjectPermission.objects.all()
    form = forms.ObjectPermissionForm


@register_model_view(ObjectPermission, "delete")
class ObjectPermissionDeleteView(generic.ObjectDeleteView):
    queryset = ObjectPermission.objects.all()
    filterset = filtersets.ObjectPermissionFilterSet


#
# Tokens
#


@register_model_view(Token, "list", path="", detail=False)
class TokenListView(generic.ObjectListView):
    queryset = Token.objects.all()
    filterset = filtersets.TokenFilterSet
    filterset_form = forms.TokenFilterSetForm
    table = tables.TokenTable


@register_model_view(Token)
class TokenView(generic.ObjectView):
    queryset = Token.objects.all()


@register_model_view(Token, "add", detail=False)
@register_model_view(Token, "edit")
class TokenEditView(generic.ObjectEditView):
    queryset = Token.objects.all()
    form = forms.TokenForm
    template_name = "users/token_edit.html"


@register_model_view(Token, "delete")
class TokenDeleteView(generic.ObjectDeleteView):
    queryset = Token.objects.all()
