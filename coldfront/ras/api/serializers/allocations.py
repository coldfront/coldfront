# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.api.serializers import (
    AttributeProfileModelSerializer,
    CustomAttributeModelSerializer,
    OrganizationalModelSerializer,
    PrimaryModelSerializer,
)
from coldfront.api.serializers.fields import RelatedObjectCountField, SerializedPKRelatedField
from coldfront.ras.models import Allocation, AllocationType, Resource
from coldfront.users.api.serializers import UserSerializer

from .projects import ProjectSerializer
from .resources import ResourceSerializer


class AllocationTypeSerializer(AttributeProfileModelSerializer, OrganizationalModelSerializer):
    allocation_count = RelatedObjectCountField("allocations")

    class Meta:
        model = AllocationType
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "description",
            "schema",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "allocation_count",
        ]
        brief_fields = ("id", "url", "display", "name", "description")


class AllocationSerializer(CustomAttributeModelSerializer, PrimaryModelSerializer):
    resource_count = RelatedObjectCountField("resources")
    allocation_type = AllocationTypeSerializer(nested=True)
    owner = UserSerializer(nested=True)
    project = ProjectSerializer(nested=True)
    resources = SerializedPKRelatedField(
        queryset=Resource.objects.all(),
        serializer=ResourceSerializer,
        nested=True,
        required=False,
        many=True,
    )

    class Meta:
        model = Allocation
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "description",
            "justification",
            "status",
            "owner",
            "allocation_type",
            "project",
            "start_date",
            "end_date",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "resource_count",
            "attributes",
            "resources",
        ]
        brief_fields = ("id", "url", "display", "id", "description", "status")
