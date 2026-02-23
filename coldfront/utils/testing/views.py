# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.test import override_settings
from django.urls import reverse

from coldfront.core.choices import ObjectChangeActionChoices
from coldfront.core.models import ObjectChange, ObjectType
from coldfront.models.features import ChangeLoggingMixin
from coldfront.users.models import ObjectPermission

from .base import ModelTestCase
from .utils import disable_warnings, get_random_string, post_data


class ModelViewTestCase(ModelTestCase):
    """
    Base TestCase for model views. Subclass to test individual views.
    """

    def _get_base_url(self):
        """
        Return the base format for a URL for the test's model. Override this to test for a model which belongs
        to a different app (e.g. testing Interfaces within the virtualization app).
        """
        return "{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    def _get_url(self, action, instance=None):
        """
        Return the URL name for a specific action and optionally a specific instance
        """
        url_format = self._get_base_url()

        # If no instance was provided, assume we don't need a unique identifier
        if instance is None:
            return reverse(url_format.format(action))

        return reverse(url_format.format(action), kwargs={"pk": instance.pk})


class ViewTestCases:
    """
    We keep any TestCases with test_* methods inside a class to prevent unittest from trying to run them.
    """

    class GetObjectViewTestCase(ModelViewTestCase):
        """
        Retrieve a single instance.
        """

        def test_get_object_anonymous(self):
            # Make the request as an unauthenticated user
            self.client.logout()
            ct = ContentType.objects.get_for_model(self.model)
            if (ct.app_label, ct.model) in settings.EXEMPT_EXCLUDE_MODELS:
                # Models listed in EXEMPT_EXCLUDE_MODELS should not be accessible to anonymous users
                with disable_warnings("django.request"):
                    response = self.client.get(self._get_queryset().first().get_absolute_url())
                    self.assertHttpStatus(response, 302)

        def test_get_object_without_permission(self):
            instance = self._get_queryset().first()

            # Try GET without permission
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.get(instance.get_absolute_url()), 403)

        def test_get_object_with_permission(self):
            instance = self._get_queryset().first()

            # Add model-level permission
            obj_perm = ObjectPermission(name="Test permission", actions=["view"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with model-level permission
            self.assertHttpStatus(self.client.get(instance.get_absolute_url()), 200)

        def test_get_object_with_constrained_permission(self):
            instance1, instance2 = self._get_queryset().all()[:2]

            # Add object-level permission
            obj_perm = ObjectPermission(name="Test permission", constraints={"pk": instance1.pk}, actions=["view"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET to permitted object
            self.assertHttpStatus(self.client.get(instance1.get_absolute_url()), 200)

            # Try GET to non-permitted object
            self.assertHttpStatus(self.client.get(instance2.get_absolute_url()), 404)

    class GetObjectChangelogViewTestCase(ModelViewTestCase):
        """
        View the changelog for an instance.
        """

        @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
        def test_get_object_changelog(self):
            url = self._get_url("changelog", self._get_queryset().first())
            response = self.client.get(url)
            self.assertHttpStatus(response, 200)

    class CreateObjectViewTestCase(ModelViewTestCase):
        """
        Create a single new instance.

        :form_data: Data to be used when creating a new object.
        """

        form_data = {}
        validation_excluded_fields = []

        def test_create_object_without_permission(self):

            # Try GET without permission
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.get(self._get_url("add")), 403)

            # Try POST without permission
            request = {
                "path": self._get_url("add"),
                "data": post_data(self.form_data),
            }
            response = self.client.post(**request)
            with disable_warnings("django.request"):
                self.assertHttpStatus(response, 403)

        @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"], EXEMPT_EXCLUDE_MODELS=[])
        def test_create_object_with_permission(self):
            # Assign unconstrained permission
            obj_perm = ObjectPermission(name="Test permission", actions=["add"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with model-level permission
            self.assertHttpStatus(self.client.get(self._get_url("add")), 200)

            # Add custom field data if the model supports it
            # if issubclass(self.model, CustomFieldsMixin):
            #    add_custom_field_data(self.form_data, self.model)

            # If supported, add a changelog message
            if issubclass(self.model, ChangeLoggingMixin):
                if "changelog_message" not in self.form_data:
                    self.form_data["changelog_message"] = get_random_string(10)

            # Try POST with model-level permission
            initial_count = self._get_queryset().count()
            request = {
                "path": self._get_url("add"),
                "data": post_data(self.form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 302)
            self.assertEqual(initial_count + 1, self._get_queryset().count())
            instance = self._get_queryset().order_by("pk").last()
            self.assertInstanceEqual(instance, self.form_data, exclude=self.validation_excluded_fields)

            # Verify ObjectChange creation
            if issubclass(self.model, ChangeLoggingMixin):
                objectchanges = ObjectChange.objects.filter(
                    changed_object_type=ContentType.objects.get_for_model(instance), changed_object_id=instance.pk
                )
                self.assertEqual(len(objectchanges), 1)
                self.assertEqual(objectchanges[0].action, ObjectChangeActionChoices.ACTION_CREATE)
                self.assertEqual(objectchanges[0].message, self.form_data["changelog_message"])

        @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"], EXEMPT_EXCLUDE_MODELS=[])
        def test_create_object_with_constrained_permission(self):

            # Assign constrained permission
            obj_perm = ObjectPermission(
                name="Test permission",
                constraints={"pk": 0},  # Dummy permission to deny all
                actions=["add"],
            )
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with object-level permission
            self.assertHttpStatus(self.client.get(self._get_url("add")), 200)

            # Try to create an object (not permitted)
            initial_count = self._get_queryset().count()
            request = {
                "path": self._get_url("add"),
                "data": post_data(self.form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 200)
            self.assertEqual(initial_count, self._get_queryset().count())  # Check that no object was created

            # Update the ObjectPermission to allow creation
            obj_perm.constraints = {"pk__gt": 0}
            obj_perm.save()

            # Try to create an object (permitted)
            request = {
                "path": self._get_url("add"),
                "data": post_data(self.form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 302)
            self.assertEqual(initial_count + 1, self._get_queryset().count())
            instance = self._get_queryset().order_by("pk").last()
            self.assertInstanceEqual(instance, self.form_data, exclude=self.validation_excluded_fields)

    class EditObjectViewTestCase(ModelViewTestCase):
        """
        Edit a single existing instance.

        :form_data: Data to be used when updating the first existing object.
        """

        form_data = {}
        validation_excluded_fields = []

        def test_edit_object_without_permission(self):
            instance = self._get_queryset().first()

            # Try GET without permission
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 403)

            # Try POST without permission
            request = {
                "path": self._get_url("edit", instance),
                "data": post_data(self.form_data),
            }
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.post(**request), 403)

        @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"], EXEMPT_EXCLUDE_MODELS=[])
        def test_edit_object_with_permission(self):
            instance = self._get_queryset().first()

            # Assign model-level permission
            obj_perm = ObjectPermission(name="Test permission", actions=["change"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with model-level permission
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance)), 200)

            # Add custom field data if the model supports it
            # if issubclass(self.model, CustomFieldsMixin):
            #    add_custom_field_data(self.form_data, self.model)

            # If supported, add a changelog message
            if issubclass(self.model, ChangeLoggingMixin):
                if "changelog_message" not in self.form_data:
                    self.form_data["changelog_message"] = get_random_string(10)

            # Try POST with model-level permission
            request = {
                "path": self._get_url("edit", instance),
                "data": post_data(self.form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 302)
            instance = self._get_queryset().get(pk=instance.pk)
            self.assertInstanceEqual(instance, self.form_data, exclude=self.validation_excluded_fields)

            # Verify ObjectChange creation
            if issubclass(self.model, ChangeLoggingMixin):
                objectchanges = ObjectChange.objects.filter(
                    changed_object_type=ContentType.objects.get_for_model(instance), changed_object_id=instance.pk
                )
                self.assertEqual(len(objectchanges), 1)
                self.assertEqual(objectchanges[0].action, ObjectChangeActionChoices.ACTION_UPDATE)
                self.assertEqual(objectchanges[0].message, self.form_data["changelog_message"])

        @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"], EXEMPT_EXCLUDE_MODELS=[])
        def test_edit_object_with_constrained_permission(self):
            instance1, instance2 = self._get_queryset().all()[:2]

            # Assign constrained permission
            obj_perm = ObjectPermission(name="Test permission", constraints={"pk": instance1.pk}, actions=["change"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with a permitted object
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance1)), 200)

            # Try GET with a non-permitted object
            self.assertHttpStatus(self.client.get(self._get_url("edit", instance2)), 404)

            # Try to edit a permitted object
            request = {
                "path": self._get_url("edit", instance1),
                "data": post_data(self.form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 302)
            instance = self._get_queryset().get(pk=instance1.pk)
            self.assertInstanceEqual(instance, self.form_data, exclude=self.validation_excluded_fields)

            # Try to edit a non-permitted object
            request = {
                "path": self._get_url("edit", instance2),
                "data": post_data(self.form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 404)

    class DeleteObjectViewTestCase(ModelViewTestCase):
        """
        Delete a single instance.
        """

        def test_delete_object_without_permission(self):
            instance = self._get_queryset().first()

            # Try GET without permission
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.get(self._get_url("delete", instance)), 403)

            # Try POST without permission
            request = {
                "path": self._get_url("delete", instance),
                "data": post_data({"confirm": True}),
            }
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.post(**request), 403)

        def test_delete_object_with_permission(self):
            instance = self._get_queryset().last()
            form_data = {"confirm": True}

            # Assign model-level permission
            obj_perm = ObjectPermission(name="Test permission", actions=["delete"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with model-level permission
            self.assertHttpStatus(self.client.get(self._get_url("delete", instance)), 200)

            # If supported, add a changelog message
            if issubclass(self.model, ChangeLoggingMixin):
                form_data["changelog_message"] = get_random_string(10)

            # Try POST with model-level permission
            request = {
                "path": self._get_url("delete", instance),
                "data": post_data(form_data),
            }
            self.assertHttpStatus(self.client.post(**request), 302)
            with self.assertRaises(ObjectDoesNotExist):
                self._get_queryset().get(pk=instance.pk)

            # Verify ObjectChange creation
            if issubclass(self.model, ChangeLoggingMixin):
                objectchanges = ObjectChange.objects.filter(
                    changed_object_type=ContentType.objects.get_for_model(instance), changed_object_id=instance.pk
                )
                self.assertEqual(len(objectchanges), 1)
                self.assertEqual(objectchanges[0].action, ObjectChangeActionChoices.ACTION_DELETE)
                self.assertEqual(objectchanges[0].message, form_data["changelog_message"])

        def test_delete_object_with_constrained_permission(self):
            instance1, instance2 = self._get_queryset().all()[:2]

            # Assign object-level permission
            obj_perm = ObjectPermission(name="Test permission", constraints={"pk": instance1.pk}, actions=["delete"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with a permitted object
            self.assertHttpStatus(self.client.get(self._get_url("delete", instance1)), 200)

            # Try GET with a non-permitted object
            self.assertHttpStatus(self.client.get(self._get_url("delete", instance2)), 404)

            # Try to delete a permitted object
            request = {
                "path": self._get_url("delete", instance1),
                "data": post_data({"confirm": True}),
            }
            self.assertHttpStatus(self.client.post(**request), 302)
            with self.assertRaises(ObjectDoesNotExist):
                self._get_queryset().get(pk=instance1.pk)

            # Try to delete a non-permitted object
            request = {
                "path": self._get_url("delete", instance2),
                "data": post_data({"confirm": True}),
            }
            self.assertHttpStatus(self.client.post(**request), 404)
            self.assertTrue(self._get_queryset().filter(pk=instance2.pk).exists())

    class ListObjectsViewTestCase(ModelViewTestCase):
        """
        Retrieve multiple instances.
        """

        def test_list_objects_anonymous(self):
            # Make the request as an unauthenticated user
            self.client.logout()
            ct = ContentType.objects.get_for_model(self.model)
            if (ct.app_label, ct.model) in settings.EXEMPT_EXCLUDE_MODELS:
                # Models listed in EXEMPT_EXCLUDE_MODELS should not be accessible to anonymous users
                with disable_warnings("django.request"):
                    response = self.client.get(self._get_url("list"))
                    self.assertHttpStatus(response, 302)

        def test_list_objects_without_permission(self):

            # Try GET without permission
            with disable_warnings("django.request"):
                self.assertHttpStatus(self.client.get(self._get_url("list")), 403)

        def test_list_objects_with_permission(self):

            # Add model-level permission
            obj_perm = ObjectPermission(name="Test permission", actions=["view"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with model-level permission
            self.assertHttpStatus(self.client.get(self._get_url("list")), 200)

        def test_list_objects_with_constrained_permission(self):
            instance1, instance2 = self._get_queryset().all()[:2]

            # Add object-level permission
            obj_perm = ObjectPermission(name="Test permission", constraints={"pk": instance1.pk}, actions=["view"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Try GET with object-level permission
            response = self.client.get(self._get_url("list"))
            self.assertHttpStatus(response, 200)
            content = str(response.content)
            self.assertIn(instance1.get_absolute_url(), content)
            self.assertNotIn(instance2.get_absolute_url(), content)

        def test_export_objects(self):
            url = self._get_url("list")

            # Add model-level permission
            obj_perm = ObjectPermission(name="Test permission", actions=["view"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))

            # Test default CSV export
            response = self.client.get(f"{url}?export")
            self.assertHttpStatus(response, 200)
            self.assertEqual(response.get("Content-Type"), "text/csv; charset=utf-8")

            # Test table-based export
            response = self.client.get(f"{url}?export=table")
            self.assertHttpStatus(response, 200)
            self.assertEqual(response.get("Content-Type"), "text/csv; charset=utf-8")

    class OrganizationalObjectViewTestCase(
        GetObjectViewTestCase,
        GetObjectChangelogViewTestCase,
        CreateObjectViewTestCase,
        EditObjectViewTestCase,
        DeleteObjectViewTestCase,
        ListObjectsViewTestCase,
    ):
        """
        TestCase suitable for all organizational objects
        """

        pass
