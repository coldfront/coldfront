# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.test import TestCase
from django.urls import reverse

from coldfront.core.test_helpers import utils
from coldfront.core.test_helpers.factories import UserFactory
from coldfront.core.user.models import UserProfile


class TestUserProfile(TestCase):
    class Data:
        """Collection of test data, separated for readability"""

        def __init__(self):
            user = UserFactory(username="submitter")

            self.initial_fields = {"user": user, "is_pi": True, "id": user.id}

            self.unsaved_object = UserProfile(**self.initial_fields)

    def setUp(self):
        self.data = self.Data()

    def test_fields_generic(self):
        profile_obj = self.data.unsaved_object
        profile_obj.save()

        self.assertEqual(1, len(UserProfile.objects.all()))

        retrieved_profile = UserProfile.objects.get(pk=profile_obj.pk)

        for item in self.data.initial_fields.items():
            (field, initial_value) = item
            with self.subTest(item=item):
                saved_value = getattr(retrieved_profile, field)
                self.assertEqual(initial_value, saved_value)
        self.assertEqual(profile_obj, retrieved_profile)

    def test_user_on_delete(self):
        profile_obj = self.data.unsaved_object
        profile_obj.save()

        self.assertEqual(1, len(UserProfile.objects.all()))

        profile_obj.user.delete()

        # expecting CASCADE
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(pk=profile_obj.pk)
        self.assertEqual(0, len(UserProfile.objects.all()))


class TestUserUpgradeAccount(TestCase):
    def setUp(self):
        self.url = reverse("user-upgrade")

    def test_logged_out_redirects_to_login(self):
        utils.test_logged_out_redirect_to_login(self, self.url)

    def test_superuser_redirects_to_profile(self):
        self.client.force_login(UserFactory(username="admin", is_superuser=True))
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("user-profile"), fetch_redirect_response=False)

    def test_pi_redirects_to_profile(self):
        user = UserFactory(username="pi")
        user.userprofile.is_pi = True
        user.userprofile.save()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("user-profile"), fetch_redirect_response=False)
