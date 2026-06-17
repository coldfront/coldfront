# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from rest_framework.routers import APIRootView

from coldfront.api.viewsets import ColdFrontModelViewSet
from coldfront.slurm import filtersets
from coldfront.slurm.models import SlurmCluster, SlurmPartition

from . import serializers


class SlurmRootView(APIRootView):
    """
    Slurm API root view
    """

    def get_view_name(self):
        return "Slurm"


class SlurmClusterViewSet(ColdFrontModelViewSet):
    queryset = SlurmCluster.objects.all()
    serializer_class = serializers.SlurmClusterSerializer
    filterset_class = filtersets.SlurmClusterFilterSet


class SlurmPartitionViewSet(ColdFrontModelViewSet):
    queryset = SlurmPartition.objects.all()
    serializer_class = serializers.SlurmPartitionSerializer
    filterset_class = filtersets.SlurmPartitionFilterSet
