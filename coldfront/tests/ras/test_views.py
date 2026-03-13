# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.ras.choices import AllocationStatusChoices, ProjectStatusChoices, ResourceStatusChoices
from coldfront.ras.models import Allocation, AllocationType, Project, ProjectUser, Resource, ResourceType
from coldfront.users.models import User
from coldfront.utils.testing import ViewTestCases, create_tags


class ProjectTestCase(ViewTestCases.OrganizationalObjectViewTestCase):
    model = Project

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

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Project X",
            "description": "A new project",
            "status": ProjectStatusChoices.STATUS_NEW,
            "tags": [t.pk for t in tags],
        }


class ResourceTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Resource

    @classmethod
    def setUpTestData(cls):

        resource_type = ResourceType.objects.create(name="Cluster")

        resources = (
            Resource(name="Resource 1", resource_type=resource_type),
            Resource(name="Resource 2", resource_type=resource_type),
            Resource(name="Resource 3", resource_type=resource_type),
        )
        for resource in resources:
            resource.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Resource X",
            "description": "A new resource",
            "resource_type": resource_type.pk,
            "status": ResourceStatusChoices.STATUS_ACTIVE,
            "tags": [t.pk for t in tags],
        }


class AllocationTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Allocation

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

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "justification": "Need resources X",
            "description": "A new Allocation",
            "owner": user.pk,
            "project": project.pk,
            "resources": [resources[0].pk, resources[1].pk],
            "allocation_type": allocation_type.pk,
            "status": AllocationStatusChoices.STATUS_ACTIVE,
            "tags": [t.pk for t in tags],
        }


class ProjectUserTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = ProjectUser

    @classmethod
    def setUpTestData(cls):
        owner = User.objects.create(username="pi")
        users = (
            User(username="User1"),
            User(username="User2"),
            User(username="User3"),
        )
        for user in users:
            user.save()

        projects = (
            Project(name="Project 1", owner=owner),
            Project(name="Project 2", owner=owner),
            Project(name="Project 3", owner=owner),
        )
        for project in projects:
            project.save()

        project_users = (
            ProjectUser(user=users[0], project=projects[0]),
            ProjectUser(user=users[1], project=projects[1]),
            ProjectUser(user=users[2], project=projects[2]),
        )
        for pu in project_users:
            pu.save()

        cls.form_data = {
            "project": projects[1].pk,
            "user": users[0].pk,
        }
