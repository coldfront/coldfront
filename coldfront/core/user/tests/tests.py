# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.test import SimpleTestCase, TestCase

from coldfront.core.test_helpers.factories import UserFactory
from coldfront.core.user.models import UserProfile
from coldfront.core.user.utils import CombinedUserSearch, split_usernames


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


class TestSplitUsernames(SimpleTestCase):
    def test_splits_on_commas_and_any_whitespace(self):
        self.assertEqual(split_usernames("alice,bob carol\tdave\neve"), ["alice", "bob", "carol", "dave", "eve"])

    def test_drops_empty_names(self):
        self.assertEqual(split_usernames("  alice, ,bob,\n"), ["alice", "bob"])

    def test_keeps_a_repeated_name_once_in_first_place(self):
        self.assertEqual(split_usernames("bob, alice\nbob alice"), ["bob", "alice"])

    def test_single_name(self):
        self.assertEqual(split_usernames("alice"), ["alice"])

    def test_empty_string(self):
        self.assertEqual(split_usernames(""), [])


class TestCombinedUserSearchSeparators(TestCase):
    def setUp(self):
        for username in ("alice", "bob", "carol"):
            UserFactory(username=username)

    def test_a_comma_separated_list_finds_every_user(self):
        context = CombinedUserSearch("alice,bob,carol", "all_fields").search()

        self.assertEqual(sorted(match["username"] for match in context["matches"]), ["alice", "bob", "carol"])
        self.assertEqual(context["number_of_usernames_searched"], 3)
        self.assertEqual(context["number_of_usernames_found"], 3)
        self.assertEqual(context["usernames_not_found"], [])

    def test_a_repeated_name_is_counted_once(self):
        context = CombinedUserSearch("alice, bob, alice", "all_fields").search()

        self.assertEqual(context["number_of_usernames_searched"], 2)
        self.assertEqual(context["number_of_usernames_found"], 2)
        self.assertEqual(context["usernames_not_found"], [])

    def test_a_getent_style_list_reports_the_missing_name(self):
        context = CombinedUserSearch("alice, bob,\tnobody", "all_fields").search()

        self.assertEqual(sorted(match["username"] for match in context["matches"]), ["alice", "bob"])
        self.assertEqual(context["usernames_not_found"], ["nobody"])
