# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.urls import reverse

from coldfront.ras.choices import AllocationStatusChoices, ProjectStatusChoices, ResourceStatusChoices
from coldfront.ras.models import Allocation, AllocationType, Project, Resource, ResourceType
from coldfront.users.models import User
from coldfront.utils.testing import APITestCase, APIViewTestCases


class AppTest(APITestCase):
    def test_root(self):

        url = reverse("ras-api:api-root")
        response = self.client.get("{}?format=api".format(url), **self.header)

        self.assertEqual(response.status_code, 200)


class ProjectTest(APIViewTestCases.APIViewTestCase):
    model = Project
    brief_fields = ["description", "display", "id", "name", "status", "url"]
    bulk_update_data = {
        "description": "New description",
    }

    @classmethod
    def setUpTestData(cls):

        users = (
            User(username="User1"),
            User(username="User2"),
            User(username="User3"),
        )
        for user in users:
            user.save()

        projects = (
            Project(name="Project 1", owner=users[0]),
            Project(name="Project 2", owner=users[1]),
            Project(name="Project 3", owner=users[2]),
        )
        for project in projects:
            project.save()

        cls.create_data = [
            {
                "name": "Project X",
                "description": "A new project",
                "owner": users[0].pk,
                "status": ProjectStatusChoices.STATUS_NEW,
            },
            {
                "name": "Project Y",
                "description": "A new project",
                "owner": users[1].pk,
                "status": ProjectStatusChoices.STATUS_NEW,
            },
            {
                "name": "Project Z",
                "description": "A new project",
                "owner": users[2].pk,
                "status": ProjectStatusChoices.STATUS_NEW,
            },
        ]


class ResourceTypeTest(APIViewTestCases.APIViewTestCase):
    model = ResourceType
    brief_fields = ["description", "display", "id", "name", "slug", "url"]
    bulk_update_data = {
        "description": "New description",
    }

    @classmethod
    def setUpTestData(cls):

        resource_types = (
            ResourceType(name="Resource Type 1", slug="type-1"),
            ResourceType(name="Resource Type 2", slug="type-2"),
            ResourceType(name="Resource Type 3", slug="type-3"),
        )
        for rt in resource_types:
            rt.save()

        cls.create_data = [
            {
                "name": "Resource Type X",
                "description": "A new type",
                "slug": "type-x",
            },
            {
                "name": "Resource Type Y",
                "description": "A new type",
                "slug": "type-y",
            },
            {
                "name": "Resource Type Z",
                "description": "A new type",
                "slug": "type-z",
            },
        ]


class ResourceTest(APIViewTestCases.APIViewTestCase):
    model = Resource
    brief_fields = ["description", "display", "id", "name", "status", "url"]
    bulk_update_data = {
        "description": "New description",
    }

    @classmethod
    def setUpTestData(cls):

        resource_type = ResourceType.objects.create(name="Cluster", slug="cluster")

        resources = (
            Resource(name="Resource 1", resource_type=resource_type),
            Resource(name="Resource 2", resource_type=resource_type),
            Resource(name="Resource 3", resource_type=resource_type),
        )
        for resource in resources:
            resource.save()

        cls.create_data = [
            {
                "name": "Resource X",
                "description": "A new resource",
                "resource_type": resource_type.pk,
                "status": ResourceStatusChoices.STATUS_ACTIVE,
            },
            {
                "name": "Resource Y",
                "description": "A new resource",
                "resource_type": resource_type.pk,
                "status": ResourceStatusChoices.STATUS_ACTIVE,
            },
            {
                "name": "Resource Z",
                "description": "A new resource",
                "resource_type": resource_type.pk,
                "status": ResourceStatusChoices.STATUS_ACTIVE,
            },
        ]


class AllocationTypeTest(APIViewTestCases.APIViewTestCase):
    model = AllocationType
    brief_fields = ["description", "display", "id", "name", "url"]
    bulk_update_data = {
        "description": "New description",
    }

    @classmethod
    def setUpTestData(cls):

        allocation_types = (
            AllocationType(name="Allocation Type 1"),
            AllocationType(name="Allocation Type 2"),
            AllocationType(name="Allocation Type 3"),
        )
        for rt in allocation_types:
            rt.save()

        cls.create_data = [
            {
                "name": "Allocation Type X",
                "description": "A new type",
            },
            {
                "name": "Allocation Type Y",
                "description": "A new type",
            },
            {
                "name": "Allocation Type Z",
                "description": "A new type",
            },
        ]


class AllocationTest(APIViewTestCases.APIViewTestCase):
    model = Allocation
    brief_fields = ["description", "display", "id", "status", "url"]
    bulk_update_data = {
        "description": "New description",
    }

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="User1")
        project = Project.objects.create(name="Project 1", owner=user)
        resource_type = ResourceType.objects.create(name="Cluster")

        resources = (
            Resource(name="Resource 1", resource_type=resource_type),
            Resource(name="Resource 2", resource_type=resource_type),
            Resource(name="Resource 3", resource_type=resource_type),
        )
        for resource in resources:
            resource.save()

        allocation_type = AllocationType.objects.create(name="Storage")

        allocations = (
            Allocation(justification="Need resources 1", project=project, owner=user, allocation_type=allocation_type),
            Allocation(justification="Need resources 2", project=project, owner=user, allocation_type=allocation_type),
            Allocation(justification="Need resources 3", project=project, owner=user, allocation_type=allocation_type),
        )
        for allocation in allocations:
            allocation.save()

        allocations[0].resources.add(resources[0])
        allocations[0].resources.add(resources[1])
        allocations[1].resources.add(resources[1])
        allocations[2].resources.add(resources[2])

        cls.create_data = [
            {
                "justification": "Need resources X",
                "description": "A new Allocation",
                "owner": user.pk,
                "project": project.pk,
                "resources": [resources[0].pk, resources[1].pk],
                "allocation_type": allocation_type.pk,
                "status": AllocationStatusChoices.STATUS_ACTIVE,
            },
            {
                "justification": "Need resources Y",
                "description": "A new Allocation",
                "owner": user.pk,
                "project": project.pk,
                "resources": [resources[0].pk],
                "allocation_type": allocation_type.pk,
                "status": AllocationStatusChoices.STATUS_ACTIVE,
            },
            {
                "justification": "Need resources Z",
                "description": "A new Allocation",
                "owner": user.pk,
                "project": project.pk,
                "resources": [resources[1].pk],
                "allocation_type": allocation_type.pk,
                "status": AllocationStatusChoices.STATUS_ACTIVE,
            },
        ]
