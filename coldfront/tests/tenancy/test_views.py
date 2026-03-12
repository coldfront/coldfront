# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.tenancy.models import Tenant, TenantGroup
from coldfront.utils.testing import ViewTestCases, create_tags


class TenantGroupTestCase(ViewTestCases.OrganizationalObjectViewTestCase):
    model = TenantGroup

    @classmethod
    def setUpTestData(cls):

        tenant_groups = (
            TenantGroup(name="Tenant Group 1", slug="tenant-group-1"),
            TenantGroup(name="Tenant Group 2", slug="tenant-group-2"),
            TenantGroup(name="Tenant Group 3", slug="tenant-group-3"),
        )
        for tenanantgroup in tenant_groups:
            tenanantgroup.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Tenant Group X",
            "slug": "tenant-group-x",
            "description": "A new tenant group",
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug,description",
            "Tenant Group 4,tenant-group-4,Fourth tenant group,",
            "Tenant Group 5,tenant-group-5,Fifth tenant group,",
            "Tenant Group 6,tenant-group-6,Sixth tenant group,",
        )

        cls.csv_update_data = (
            "id,name,description,comments",
            f"{tenant_groups[0].pk},Tenant Group 7,Fourth tenant group7,",
            f"{tenant_groups[1].pk},Tenant Group 8,Fifth tenant group8,",
            f"{tenant_groups[2].pk},Tenant Group 0,Sixth tenant group9,",
        )

        cls.bulk_edit_data = {
            "description": "New description",
        }


class TenantTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Tenant

    @classmethod
    def setUpTestData(cls):

        tenant_groups = (
            TenantGroup(
                name="Tenant Group 1",
                slug="tenant-group-1",
            ),
            TenantGroup(
                name="Tenant Group 2",
                slug="tenant-group-2",
            ),
        )
        for tenanantgroup in tenant_groups:
            tenanantgroup.save()

        tenants = (
            Tenant(
                name="Tenant 1",
                slug="tenant-1",
                group=tenant_groups[0],
            ),
            Tenant(
                name="Tenant 2",
                slug="tenant-2",
                group=tenant_groups[0],
            ),
            Tenant(
                name="Tenant 3",
                slug="tenant-3",
                group=tenant_groups[0],
            ),
            Tenant(
                name="Tenant 4",
                slug="tenant-4",
                group=tenant_groups[0],
            ),
            Tenant(
                name="Tenant 5",
                slug="tenant-5",
                group=tenant_groups[0],
            ),
        )
        Tenant.objects.bulk_create(tenants)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Tenant X",
            "slug": "tenant-x",
            "group": tenant_groups[1].pk,
            "description": "A new tenant",
            "tags": [t.pk for t in tags],
        }
