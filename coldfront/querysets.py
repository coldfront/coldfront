# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.db.models import Manager
from mptt.managers import TreeManager as TreeManager_
from mptt.querysets import TreeQuerySet as TreeQuerySet_

from coldfront.users.querysets import RestrictedQuerySet

__all__ = (
    "TreeQuerySet",
    "TreeManager",
)


class TreeQuerySet(TreeQuerySet_, RestrictedQuerySet):
    """
    Mate django-mptt's TreeQuerySet with our RestrictedQuerySet for permissions enforcement.
    """

    pass


class TreeManager(Manager.from_queryset(TreeQuerySet), TreeManager_):
    """
    Extend django-mptt's TreeManager to incorporate RestrictedQuerySet().
    """

    pass
