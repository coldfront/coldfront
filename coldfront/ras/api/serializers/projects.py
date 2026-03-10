# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.api.serializers import OrganizationalModelSerializer
from coldfront.api.serializers.fields import RelatedObjectCountField
from coldfront.ras.models import Project
from coldfront.users.api.serializers import UserSerializer


class ProjectSerializer(OrganizationalModelSerializer):
    allocation_count = RelatedObjectCountField("allocations")
    owner = UserSerializer(nested=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "description",
            "status",
            "tags",
            "owner",
            "custom_fields",
            "created",
            "last_updated",
            "allocation_count",
        ]
        brief_fields = ("id", "url", "display", "name", "description", "status")
