# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.api.serializers import (
    CustomAttributeModelSerializer,
    PrimaryModelSerializer,
)
from coldfront.ras.models import Allocation, AllocationUser
from coldfront.users.api.serializers import UserSerializer

from .projects import ProjectSerializer
from .resources import ResourceSerializer


class AllocationSerializer(CustomAttributeModelSerializer, PrimaryModelSerializer):
    owner = UserSerializer(nested=True)
    project = ProjectSerializer(nested=True)
    resource = ResourceSerializer(nested=True)

    class Meta:
        model = Allocation
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "slug",
            "description",
            "justification",
            "status",
            "owner",
            "project",
            "resource",
            "start_date",
            "end_date",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "attributes",
        ]
        brief_fields = ("id", "url", "display", "id", "slug", "description", "status")


class AllocationUserSerializer(PrimaryModelSerializer):
    user = UserSerializer(nested=True)
    allocation = AllocationSerializer(nested=True)

    class Meta:
        model = AllocationUser
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "user",
            "allocation",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ("id", "url", "display", "user", "allocation")
