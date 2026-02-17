# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.test import TestCase

from coldfront.core.models import ObjectType
from coldfront.tenancy.models import Tenant, TenantGroup


class BasicFeaturesTest(TestCase):
    def test_has_feature(self):
        """
        Test the functionality of the ObjectType.has_feature() utility function.
        """
        # Sanity checking
        self.assertTrue(hasattr(Tenant, "clone"), "Invalid test?")

        self.assertTrue(ObjectType.has_feature(Tenant, "cloning"))
        self.assertTrue(ObjectType.has_feature(Tenant, "change_logging"))

    def test_get_model_features(self):
        """
        Check that ObjectType.get_model_features() returns the expected features for a model.
        """
        # Sanity checking
        self.assertTrue(hasattr(Tenant, "clone"), "Invalid test?")

        features = ObjectType.get_model_features(Tenant)
        self.assertIn("cloning", features)
        self.assertIn("change_logging", features)

    def test_cloningmixin(self):
        """
        Test basic functionality of the CloningMixin
        """
        group = TenantGroup.objects.create(name="Test Group", slug="test-group")
        tenant = Tenant.objects.create(name="Test", description="test desc", group=group)
        attrs = tenant.clone()
        self.assertEqual(attrs["group"], tenant.group_id)
        self.assertEqual(attrs["description"], tenant.description)
        self.assertNotIn("name", attrs)
        self.assertNotIn("slug", attrs)
