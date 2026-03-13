# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from .allocations import (
    AllocationDeleteView,
    AllocationEditView,
    AllocationListView,
    AllocationTypeDeleteView,
    AllocationTypeEditView,
    AllocationTypeListView,
    AllocationTypeView,
    AllocationView,
)
from .projects import (
    ProjectAllocationsView,
    ProjectDeleteView,
    ProjectEditView,
    ProjectListView,
    ProjectView,
)
from .resources import (
    ResourceDeleteView,
    ResourceEditView,
    ResourceListView,
    ResourceTypeDeleteView,
    ResourceTypeEditView,
    ResourceTypeListView,
    ResourceTypeView,
    ResourceView,
)

__all__ = (
    "AllocationDeleteView",
    "AllocationEditView",
    "AllocationListView",
    "AllocationTypeDeleteView",
    "AllocationTypeEditView",
    "AllocationTypeListView",
    "AllocationTypeView",
    "AllocationView",
    "ProjectAllocationsView",
    "ProjectDeleteView",
    "ProjectEditView",
    "ProjectListView",
    "ProjectView",
    "ResourceDeleteView",
    "ResourceEditView",
    "ResourceListView",
    "ResourceTypeDeleteView",
    "ResourceTypeEditView",
    "ResourceTypeListView",
    "ResourceTypeView",
    "ResourceView",
)
