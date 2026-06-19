# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.api.serializers import AllocatableResourceModelSerializer, PrimaryModelSerializer
from coldfront.api.serializers.fields import RelatedObjectCountField
from coldfront.slurm.models import SlurmCluster, SlurmPartition
from coldfront.tenancy.api.serializers.tenants import TenantSerializer

from .nested import NestedSlurmClusterSerializer


class SlurmClusterSerializer(AllocatableResourceModelSerializer, PrimaryModelSerializer):
    tenant = TenantSerializer(nested=True, required=False, allow_null=True, default=None)
    partition_count = RelatedObjectCountField("partitions")

    class Meta:
        model = SlurmCluster
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "tenant",
            "description",
            "locked",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "partition_count",
            "schema",
        ]
        brief_fields = ("id", "url", "display", "name", "description", "locked")


class SlurmPartitionSerializer(AllocatableResourceModelSerializer, PrimaryModelSerializer):
    cluster = NestedSlurmClusterSerializer(nested=True)

    class Meta:
        model = SlurmPartition
        fields = [
            "id",
            "url",
            "display_url",
            "display",
            "cluster",
            "name",
            "description",
            "locked",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "schema",
        ]
        brief_fields = ("id", "url", "display", "name", "description", "locked")
