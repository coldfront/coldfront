# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.db.models import Count, OuterRef, QuerySet, Subquery
from django.db.models.functions import Coalesce

from coldfront.users.querysets import TreeManager

__all__ = (
    "count_related",
    "reapply_model_ordering",
)


def count_related(model, field):
    """
    Return a Subquery suitable for annotating a child object count.
    """
    subquery = Subquery(
        model.objects.filter(**{field: OuterRef("pk")}).order_by().values(field).annotate(c=Count("*")).values("c")
    )

    return Coalesce(subquery, 0)


def reapply_model_ordering(queryset: QuerySet) -> QuerySet:
    """
    Reapply model-level ordering in case it has been lost through .annotate().
    https://code.djangoproject.com/ticket/32811
    """
    # MPTT-based models are exempt from this; use caution when annotating querysets of these models
    if any(isinstance(manager, TreeManager) for manager in queryset.model._meta.local_managers):
        return queryset
    elif queryset.ordered:
        return queryset

    ordering = queryset.model._meta.ordering
    return queryset.order_by(*ordering)
