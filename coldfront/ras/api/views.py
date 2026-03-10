# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rest_framework.routers import APIRootView

from coldfront.api.viewsets import ColdFrontModelViewSet
from coldfront.ras import filtersets
from coldfront.ras.models import Allocation, AllocationType, Project, Resource, ResourceType

from . import serializers


class RASRootView(APIRootView):
    """
    RAS API root view
    """

    def get_view_name(self):
        return "RAS"


#
# Projects
#


class ProjectViewSet(ColdFrontModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filterset_class = filtersets.ProjectFilterSet


#
# Resources
#


class ResourceViewSet(ColdFrontModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    filterset_class = filtersets.ResourceFilterSet


class ResourceTypeViewSet(ColdFrontModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = serializers.ResourceTypeSerializer
    filterset_class = filtersets.ResourceTypeFilterSet


#
# Allocations
#


class AllocationViewSet(ColdFrontModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = serializers.AllocationSerializer
    filterset_class = filtersets.AllocationFilterSet


class AllocationTypeViewSet(ColdFrontModelViewSet):
    queryset = AllocationType.objects.all()
    serializer_class = serializers.AllocationTypeSerializer
    filterset_class = filtersets.AllocationTypeFilterSet
