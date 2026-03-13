# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.api.serializers import OrganizationalModelSerializer, PrimaryModelSerializer
from coldfront.api.serializers.fields import RelatedObjectCountField
from coldfront.ras.models import Project, ProjectUser
from coldfront.tenancy.api.serializers import TenantSerializer
from coldfront.users.api.serializers import UserSerializer


class ProjectSerializer(OrganizationalModelSerializer):
    allocation_count = RelatedObjectCountField("allocations")
    user_count = RelatedObjectCountField("users")
    owner = UserSerializer(nested=True)
    tenant = TenantSerializer(
        nested=True,
        allow_null=True,
        required=False,
        default=None,
    )

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
            "tenant",
            "custom_fields",
            "created",
            "last_updated",
            "allocation_count",
            "user_count",
        ]
        brief_fields = ("id", "url", "display", "name", "description", "status")


class ProjectUserSerializer(PrimaryModelSerializer):
    user = UserSerializer(nested=True)
    project = ProjectSerializer(nested=True)

    class Meta:
        model = ProjectUser
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "user",
            "project",
            "custom_fields",
            "created",
            "last_updated",
        ]
        brief_fields = ("id", "url", "display", "user", "project")
