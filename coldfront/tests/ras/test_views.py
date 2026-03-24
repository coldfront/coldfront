# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.core.choices import CSVDelimiterChoices, ImportFormatChoices
from coldfront.ras.choices import AllocationStatusChoices, ProjectStatusChoices, ResourceStatusChoices
from coldfront.ras.models import (
    Allocation,
    AllocationUser,
    Project,
    ProjectUser,
    Resource,
    ResourceType,
)
from coldfront.tenancy.models import Tenant
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
            "status": ProjectStatusChoices.STATUS_ACTIVE,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,description,status,owner",
            "Project 4,Fourth project,active,User1",
            "Project 5,Fifth project,active,User2",
            "Project 6,Sixth project,active,User3",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{projects[0].pk},Project 7,Fourth project7",
            f"{projects[1].pk},Project 8,Fifth project8",
            f"{projects[2].pk},Project 9,Sixth project9",
        )

    def test_tenant_validation_enforced(self):
        """
        Test that editing a tenant on a project is restricted.
        """
        tenant = Tenant.objects.create(name="Tenant 1")

        self.add_permissions("ras.add_project")
        data = {
            "name": "Project X",
            "description": "A new project",
            "status": ProjectStatusChoices.STATUS_ACTIVE,
            "tenant": tenant.pk,
        }

        request = {
            "path": self._get_url("add"),
            "data": data,
        }

        # No perms
        response = self.client.post(**request)
        self.assertHttpStatus(response, 200)

        # With perms
        self.add_permissions("tenancy.view_tenant")
        response = self.client.post(**request)
        self.assertHttpStatus(response, 302)


class ResourceTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Resource

    @classmethod
    def setUpTestData(cls):

        resource_type = ResourceType.objects.create(name="Cluster")

        resources = (
            Resource(name="Resource 1", slug="r-1", resource_type=resource_type),
            Resource(name="Resource 2", slug="r-2", resource_type=resource_type),
            Resource(name="Resource 3", slug="r-3", resource_type=resource_type),
        )
        for resource in resources:
            resource.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Resource X",
            "slug": "r-x",
            "description": "A new resource",
            "resource_type": resource_type.pk,
            "status": ResourceStatusChoices.STATUS_ACTIVE,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug,description,status,resource_type",
            "Resource 4,r-4,Fourth resource,active,Cluster",
            "Resource 5,r-5,Fifth resource,active,Cluster",
            "Resource 6,r-6,Sixth resource,active,Cluster",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{resources[0].pk},Resource 7,Seven resource7",
            f"{resources[1].pk},Resource 8,Eight resource8",
            f"{resources[2].pk},Resource 9,Nine resource9",
        )


class AllocationTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Allocation

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="User1")
        project = Project.objects.create(name="Project 1", owner=user)
        resource_type = ResourceType.objects.create(name="Cluster")

        resources = (
            Resource(name="Resource 1", slug="r-1", resource_type=resource_type),
            Resource(name="Resource 2", slug="r-2", resource_type=resource_type),
            Resource(name="Resource 3", slug="r-3", resource_type=resource_type),
        )
        for resource in resources:
            resource.save()

        allocations = (
            Allocation(justification="Need resources 1", project=project, owner=user, resource=resources[0]),
            Allocation(justification="Need resources 2", project=project, owner=user, resource=resources[1]),
            Allocation(justification="Need resources 3", project=project, owner=user, resource=resources[2]),
        )
        for allocation in allocations:
            allocation.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "justification": "Need resources X",
            "description": "A new Allocation",
            "owner": user.pk,
            "project": project.pk,
            "resource": resources[0].pk,
            "status": AllocationStatusChoices.STATUS_ACTIVE,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "justification,description,status,owner,project,resource",
            "need resources4,Fourth allocation,active,User1,Project 1,Resource 1",
            "need resources5,Fifth allocation,active,User1,Project 1,Resource 2",
            "need resources6,Sixth allocation,active,User1,Project 1,Resource 3",
        )

        cls.csv_update_data = (
            "id,description",
            f"{allocations[0].pk},Fourth allocation7",
            f"{allocations[1].pk},Fifth allocation8",
            f"{allocations[2].pk},Sixth allocation9",
        )


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
            Project(name="Project 4", owner=owner),
        )
        for project in projects:
            project.save()

        project_users = (
            ProjectUser(user=users[0], project=projects[0]),
            ProjectUser(user=users[1], project=projects[0]),
            ProjectUser(user=users[2], project=projects[0]),
        )
        for pu in project_users:
            pu.save()

        cls.form_data = {
            "project": projects[1].pk,
            "user": users[0].pk,
        }

        cls.csv_data = (
            "user,project",
            "User1,Project 3",
            "User2,Project 3",
            "User3,Project 3",
        )

        cls.csv_update_data = (
            "id,project",
            f"{project_users[0].pk},Project 4",
            f"{project_users[1].pk},Project 4",
            f"{project_users[2].pk},Project 4",
        )


class AllocationUserTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = AllocationUser

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

        project = Project.objects.create(name="Project 1", owner=owner)

        project_users = (
            ProjectUser(user=users[0], project=project),
            ProjectUser(user=users[1], project=project),
            ProjectUser(user=users[2], project=project),
        )
        for pu in project_users:
            pu.save()

        resource_type = ResourceType.objects.create(name="Cluster")
        resources = (
            Resource(name="Resource 1", slug="r-1", resource_type=resource_type),
            Resource(name="Resource 2", slug="r-2", resource_type=resource_type),
            Resource(name="Resource 3", slug="r-3", resource_type=resource_type),
        )
        for resource in resources:
            resource.save()

        allocations = (
            Allocation(justification="Need resources 1", project=project, owner=owner, resource=resources[0]),
            Allocation(justification="Need resources 2", project=project, owner=owner, resource=resources[1]),
            Allocation(justification="Need resources 3", project=project, owner=owner, resource=resources[1]),
            Allocation(justification="Need resources 4", project=project, owner=owner, resource=resources[2]),
        )
        for allocation in allocations:
            allocation.save()

        allocation_users = (
            AllocationUser(user=users[0], allocation=allocations[0]),
            AllocationUser(user=users[1], allocation=allocations[0]),
            AllocationUser(user=users[2], allocation=allocations[0]),
        )
        for au in allocation_users:
            au.save()

        cls.form_data = {
            "allocation": allocations[1].pk,
            "user": users[0].pk,
        }

        cls.csv_data = (
            "user,allocation.slug",
            f"User1,{allocations[2].slug}",
            f"User2,{allocations[2].slug}",
            f"User3,{allocations[2].slug}",
        )

        cls.csv_update_data = (
            "id,allocation",
            f"{allocation_users[0].pk},{allocations[3].slug}",
            f"{allocation_users[1].pk},{allocations[3].slug}",
            f"{allocation_users[2].pk},{allocations[3].slug}",
        )

    def test_adding_users_from_different_project(self):
        """
        Test that users added to an allocation must belong to the same project is enforced
        """

        initial_count = AllocationUser.objects.count()
        user = User.objects.create(username="UserNew")
        project = Project.objects.create(name="Project New", owner=user)
        ProjectUser(user=user, project=project)

        allocation = Allocation.objects.first()
        self.assertNotEqual(project, allocation.project)

        self.add_permissions("ras.add_allocationuser", "ras.view_allocation", "users.view_user")

        data = {
            "allocation": allocation.pk,
            "user": user.pk,
        }

        request = {
            "path": self._get_url("add"),
            "data": data,
        }

        response = self.client.post(**request)
        self.assertHttpStatus(response, 200)
        self.assertEqual(initial_count, AllocationUser.objects.count())

        csv_data = (
            "user,allocation.slug",
            f"{user.username},{allocation.slug}",
        )

        data = {
            "data": csv_data,
            "format": ImportFormatChoices.CSV,
            "csv_delimiter": CSVDelimiterChoices.AUTO,
        }

        request = {
            "path": self._get_url("bulk_import"),
            "data": data,
        }

        response = self.client.post(**request)
        self.assertHttpStatus(response, 302)
        self.assertEqual(initial_count, AllocationUser.objects.count())
