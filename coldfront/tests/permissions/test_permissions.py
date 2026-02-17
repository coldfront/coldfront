# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.test import RequestFactory, TestCase

from coldfront.auth.mixins import ObjectPermissionMixin, ObjectPermissionRequiredMixin
from coldfront.core.models import ObjectType
from coldfront.users.models import Group, ObjectPermission, User
from coldfront.users.permissions import get_permission_for_model


class DummyUserView(ObjectPermissionRequiredMixin):
    queryset = User.objects.all()

    def get_required_permission(self):
        return get_permission_for_model(self.queryset.model, "view")


class ObjectPermissionTest(TestCase):
    def test_actions(self):
        """
        Test ObjectPermission actions, ObjectPermissionsMixin, and RestrictedQuerySet
        """
        groups = (
            Group(name="Group 1"),
            Group(name="Group 2"),
            Group(name="Group 3"),
        )
        Group.objects.bulk_create(groups)

        users = (
            User(username="User1"),
            User(username="User2"),
            User(username="User3"),
        )
        User.objects.bulk_create(users)

        object_types = (
            ObjectType.objects.get(app_label="users", model="user"),
            ObjectType.objects.get(app_label="users", model="group"),
        )

        permissions = (
            ObjectPermission(
                name="Permission 1",
                actions={"view": True, "add": True, "change": True, "delete": True},
                constraints={"username": "User3"},
                description="foobar1",
            ),
            ObjectPermission(
                name="Permission 2",
                actions={"view": True},
            ),
            ObjectPermission(name="Permission 3", actions={"add": True}, enabled=False),
        )

        ObjectPermission.objects.bulk_create(permissions)
        for i in range(0, 3):
            permissions[i].groups.set([groups[i]])
            permissions[i].users.set([users[i]])
            permissions[i].object_types.set(object_types)

        self.assertTrue(ObjectPermission.objects.get(name="Permission 1").can_delete)
        self.assertFalse(ObjectPermission.objects.get(name="Permission 2").can_delete)
        self.assertFalse(ObjectPermission.objects.get(name="Permission 3").can_view)

        opm = ObjectPermissionMixin()
        self.assertTrue(opm.has_perm(users[0], "users.change_user", obj=users[2]))
        self.assertFalse(opm.has_perm(users[0], "users.change_user", obj=users[1]))
        self.assertFalse(opm.has_perm(users[0], "users.change_user", obj=users[0]))
        self.assertTrue(opm.has_perm(users[0], "users.add_user"))
        self.assertTrue(opm.has_perm(users[1], "users.view_group"))
        self.assertTrue(opm.has_perm(users[1], "users.view_group", obj=groups[1]))
        self.assertFalse(opm.has_perm(users[1], "users.add_group"))
        self.assertFalse(opm.has_perm(users[1], "users.change_group", obj=groups[0]))
        self.assertFalse(opm.has_perm(users[2], "users.add_user"))

        self.assertEqual(User.objects.restrict(users[0], "view").count(), 1)
        self.assertEqual(User.objects.restrict(users[1], "view").count(), 3)
        self.assertEqual(User.objects.restrict(users[2], "view").count(), 0)

        view = DummyUserView()
        view.request = RequestFactory().get("/users/user/")
        view.request.user = users[0]
        self.assertTrue(view.has_permission())
        view.request.user = users[2]
        self.assertFalse(view.has_permission())
