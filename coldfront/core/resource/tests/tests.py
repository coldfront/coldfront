# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Create your tests here.

import logging
import sys

from django.core.exceptions import ValidationError
from django.test import TestCase

from coldfront.core.test_helpers.factories import (
    RAttributeTypeFactory,
    ResourceAttributeFactory,
    ResourceAttributeTypeFactory,
)

logging.disable(logging.CRITICAL)


class ResourceAttributeModelCleanMethodTests(TestCase):
    def _test_clean(
        self, resource_attribute_type_name: str, resource_attribute_values: list, expect_validation_error: bool
    ):
        attribute_type = RAttributeTypeFactory(name=resource_attribute_type_name)
        resource_attribute_type = ResourceAttributeTypeFactory(attribute_type=attribute_type)
        resource_attribute = ResourceAttributeFactory(resource_attribute_type=resource_attribute_type)
        for value in resource_attribute_values:
            with self.subTest(value=value):
                if not isinstance(value, str):
                    raise TypeError("resource attribute value must be a string")
                resource_attribute.value = value
                if expect_validation_error:
                    with self.assertRaises(ValidationError):
                        resource_attribute.clean()
                else:
                    resource_attribute.clean()

    def test_expect_int_given_int(self):
        self._test_clean("Int", ["0", "1", str(sys.maxsize)], False)

    def test_expect_int_given_float(self):
        # FIXME -1 should be a valid int
        self._test_clean("Int", ["-1", "-1.0", "0.0", "1.0", "2e30"], True)

    def test_expect_int_given_garbage(self):
        self._test_clean("Int", ["foobar", "", " ", "\0", "1j"], True)

    def test_expect_public_private_given_public_private(self):
        self._test_clean("Public/Private", ["Public", "Private"], False)

    def test_expect_public_private_given_garbage(self):
        self._test_clean(
            "Public/Private",
            ["foobar", "", " ", "\0", "1", "1.0", "2e30", "1j", "public", "private", "PUBLIC", "PRIVATE"],
            True,
        )

    def test_expect_active_inactive_given_active_inactive(self):
        self._test_clean("Active/Inactive", ["Active", "Inactive"], False)

    def test_expect_active_inactive_given_garbage(self):
        self._test_clean(
            "Active/Inactive",
            ["foobar", "", " ", "\0", "1", "1.0", "2e30", "1j", "active", "inactive", "ACTIVE", "INACTIVE"],
            True,
        )

    def test_expect_date_given_date(self):
        # FIXME date format is different from project, allocation
        self._test_clean("Date", ["01/01/1970"], False)

    def test_expect_date_given_garbage(self):
        self._test_clean("Date", ["foobar", "", " ", "\0", "1", "1.0", "2e30", "1j"], True)
