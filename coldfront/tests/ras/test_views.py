# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType

from coldfront.ras.choices import AllocationStatusChoices, ResourceStatusChoices
from coldfront.ras.models import (
    Allocation,
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
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,description,owner",
            "Project 4,Fourth project,User1",
            "Project 5,Fifth project,User2",
            "Project 6,Sixth project,User3",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{projects[0].pk},Project 7,Fourth project7",
            f"{projects[1].pk},Project 8,Fifth project8",
            f"{projects[2].pk},Project 9,Sixth project9",
        )

        cls.bulk_edit_form_data = {
            "description": "Updated project",
        }

    def test_tenant_validation_enforced(self):
        """
        Test that editing a tenant on a project is restricted.
        """
        tenant = Tenant.objects.create(name="Tenant 1")

        self.add_permissions("ras.add_project")
        data = {
            "name": "Project X",
            "description": "A new project",
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

        cls.bulk_edit_form_data = {
            "description": "Updated resource",
            "locked": True,
        }


class AllocationTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Allocation
    validation_excluded_fields = ("resource_object",)

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

        resource_ct = ContentType.objects.get_for_model(Resource)
        allocations = (
            Allocation(
                justification="Need resources 1",
                project=project,
                owner=user,
                resource_object_type=resource_ct,
                resource_object_id=resources[0].pk,
            ),
            Allocation(
                justification="Need resources 2",
                project=project,
                owner=user,
                resource_object_type=resource_ct,
                resource_object_id=resources[1].pk,
            ),
            Allocation(
                justification="Need resources 3",
                project=project,
                owner=user,
                resource_object_type=resource_ct,
                resource_object_id=resources[2].pk,
            ),
        )
        for allocation in allocations:
            allocation.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        resource_ct = ContentType.objects.get_for_model(Resource)
        cls.form_data = {
            "justification": "Need resources X",
            "description": "A new Allocation",
            "owner": user.pk,
            "project": project.pk,
            "resource_object": f"{resource_ct.pk}:{resources[0].pk}",
            "status": AllocationStatusChoices.STATUS_NEW,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "justification,description,status,owner,project,resource_object",
            "need resources4,Fourth allocation,active,User1,Project 1,ras.resource:Resource 1",
            "need resources5,Fifth allocation,active,User1,Project 1,ras.resource:Resource 2",
            "need resources6,Sixth allocation,active,User1,Project 1,ras.resource:Resource 3",
        )

        cls.csv_update_data = (
            "id,description",
            f"{allocations[0].pk},Fourth allocation7",
            f"{allocations[1].pk},Fifth allocation8",
            f"{allocations[2].pk},Sixth allocation9",
        )

        cls.bulk_edit_form_data = {
            "description": "Updated allocation",
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

        cls.bulk_edit_form_data = {
            "project": projects[2].pk,
        }
