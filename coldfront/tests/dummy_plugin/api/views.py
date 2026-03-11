# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from rest_framework.viewsets import ModelViewSet

from coldfront.tests.dummy_plugin.models import DummyModel

from .serializers import DummySerializer


class DummyViewSet(ModelViewSet):
    queryset = DummyModel.objects.all()
    serializer_class = DummySerializer
