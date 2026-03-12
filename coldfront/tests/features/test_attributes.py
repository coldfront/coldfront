# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase

from coldfront.ras.filtersets import ResourceFilterSet
from coldfront.ras.models import Resource, ResourceType


class ResourceTypeTestCase(TestCase):
    queryset = Resource.objects.all()
    filterset = ResourceFilterSet

    PROFILE_SCHEMA = {
        "properties": {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "number": {"type": "number"},
            "boolean": {"type": "boolean"},
        }
    }

    @classmethod
    def setUpTestData(cls):

        resource_types = (
            ResourceType(name="Resource Type 1", slug="rt-1", schema=cls.PROFILE_SCHEMA),
            ResourceType(name="Resource Type 2", slug="rt-2", schema=cls.PROFILE_SCHEMA),
            ResourceType(name="Resource Type 3", slug="rt-3", schema=cls.PROFILE_SCHEMA),
        )
        ResourceType.objects.bulk_create(resource_types)

        resources = (
            Resource(
                name="Resource 1",
                resource_type=resource_types[0],
                attribute_data={
                    "string": "string1",
                    "integer": 1,
                    "number": 1.0,
                    "boolean": True,
                },
            ),
            Resource(
                name="Resource 2",
                resource_type=resource_types[1],
                attribute_data={
                    "string": "string2",
                    "integer": 2,
                    "number": 2.0,
                    "boolean": False,
                },
            ),
            Resource(
                name="Resource 3",
                resource_type=resource_types[2],
                attribute_data={
                    "string": "string3",
                    "integer": 3,
                    "number": 3.0,
                    "boolean": None,
                },
            ),
        )
        for resource in resources:
            resource.save()

    def test_resource_attributes(self):
        params = {"attr_string": "string1"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"attr_integer": "1"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"attr_number": "2.0"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"attr_boolean": "true"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
