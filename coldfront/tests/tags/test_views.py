# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.contrib.contenttypes.models import ContentType

from coldfront.core.models import Tag
from coldfront.tenancy.models import Tenant
from coldfront.utils.testing import ViewTestCases


class TagTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Tag

    @classmethod
    def setUpTestData(cls):

        tenant_ct = ContentType.objects.get_for_model(Tenant)

        tags = (
            Tag(name="Tag 1", slug="tag-1"),
            Tag(name="Tag 2", slug="tag-2", weight=1),
            Tag(name="Tag 3", slug="tag-3", weight=32767),
        )
        Tag.objects.bulk_create(tags)

        cls.form_data = {
            "name": "Tag X",
            "slug": "tag-x",
            "color": "c0c0c0",
            "object_types": [tenant_ct.pk],
            "weight": 11,
        }
