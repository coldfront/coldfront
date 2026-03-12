# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.api.serializers import (
    AttributeProfileModelSerializer,
    CustomAttributeModelSerializer,
    OrganizationalModelSerializer,
    PrimaryModelSerializer,
)
from coldfront.api.serializers.fields import RelatedObjectCountField
from coldfront.ras.models import Resource, ResourceType


class ResourceTypeSerializer(AttributeProfileModelSerializer, OrganizationalModelSerializer):
    resource_count = RelatedObjectCountField("resources")

    class Meta:
        model = ResourceType
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "slug",
            "description",
            "color",
            "schema",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "resource_count",
        ]
        brief_fields = ("id", "url", "display", "name", "description", "slug")


class ResourceSerializer(CustomAttributeModelSerializer, PrimaryModelSerializer):
    allocation_count = RelatedObjectCountField("allocations")
    resource_type = ResourceTypeSerializer(nested=True)

    class Meta:
        model = Resource
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "description",
            "status",
            "resource_type",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "allocation_count",
            "attributes",
        ]
        brief_fields = ("id", "url", "display", "name", "description", "status")
