# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from rest_framework.routers import APIRootView

from coldfront.api.viewsets import ColdFrontModelViewSet
from coldfront.slurm import filtersets
from coldfront.slurm.models import (
    SlurmAccount,
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmQOS,
    SlurmUser,
)

from . import serializers


class SlurmRootView(APIRootView):
    """
    Slurm API root view
    """

    def get_view_name(self):
        return "Slurm"


class SlurmQOSViewSet(ColdFrontModelViewSet):
    queryset = SlurmQOS.objects.all()
    serializer_class = serializers.SlurmQOSSerializer
    filterset_class = filtersets.SlurmQOSFilterSet


class SlurmClusterViewSet(ColdFrontModelViewSet):
    queryset = SlurmCluster.objects.all()
    serializer_class = serializers.SlurmClusterSerializer
    filterset_class = filtersets.SlurmClusterFilterSet


class SlurmPartitionViewSet(ColdFrontModelViewSet):
    queryset = SlurmPartition.objects.all()
    serializer_class = serializers.SlurmPartitionSerializer
    filterset_class = filtersets.SlurmPartitionFilterSet


class SlurmAccountViewSet(ColdFrontModelViewSet):
    queryset = SlurmAccount.objects.all()
    serializer_class = serializers.SlurmAccountSerializer
    filterset_class = filtersets.SlurmAccountFilterSet


class SlurmAssociationViewSet(ColdFrontModelViewSet):
    queryset = SlurmAssociation.objects.all()
    serializer_class = serializers.SlurmAssociationSerializer
    filterset_class = filtersets.SlurmAssociationFilterSet


class SlurmUserViewSet(ColdFrontModelViewSet):
    queryset = SlurmUser.objects.all()
    serializer_class = serializers.SlurmUserSerializer
    filterset_class = filtersets.SlurmUserFilterSet
