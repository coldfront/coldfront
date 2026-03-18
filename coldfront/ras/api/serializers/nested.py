# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from rest_framework import serializers

from coldfront.api.serializers import WritableNestedSerializer
from coldfront.tenancy import models

__all__ = ("NestedResourceSerializer",)


class NestedResourceSerializer(WritableNestedSerializer):
    _depth = serializers.IntegerField(source="level", read_only=True)

    class Meta:
        model = models.TenantGroup
        fields = ["id", "url", "display_url", "display", "name", "slug", "_depth"]
