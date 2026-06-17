# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0


from coldfront.api.serializers import WritableNestedSerializer
from coldfront.slurm import models

__all__ = (
    "NestedSlurmClusterSerializer",
    "NestedSlurmPartitionSerializer",
)


class NestedSlurmClusterSerializer(WritableNestedSerializer):
    class Meta:
        model = models.SlurmCluster
        fields = ["id", "url", "display_url", "display", "name"]
        brief_fields = ("id", "url", "display", "name")


class NestedSlurmPartitionSerializer(WritableNestedSerializer):
    class Meta:
        model = models.SlurmPartition
        fields = ["id", "url", "display_url", "display", "name"]
        brief_fields = ("id", "url", "display", "name")
