# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from rest_framework.serializers import ModelSerializer

from coldfront.tests.dummy_plugin.models import DummyModel


class DummySerializer(ModelSerializer):
    class Meta:
        model = DummyModel
        fields = ("id", "name", "number")
