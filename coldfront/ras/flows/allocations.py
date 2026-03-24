# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from viewflow import fsm, this

from coldfront.flows import ColdFrontFlow
from coldfront.ras import object_actions as actions
from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.signals import allocation_status_change


class AllocationStatusFlow(ColdFrontFlow):
    """
    Allocation Status workflow defines the transitions between the statuses of an Allocation.
    """

    status = fsm.State(AllocationStatusChoices, default=AllocationStatusChoices.STATUS_NEW)
    label = "Allocation"
    actions = (
        actions.ApproveObject,
        actions.DenyObject,
        actions.ActivateObject,
        actions.RenewObject,
        actions.RevokeObject,
    )

    def __init__(self, allocation):
        self.allocation = allocation

    @status.setter()
    def _set_allocation_status(self, value):
        self.allocation.status = value

    @status.getter()
    def _get_allocation_status(self):
        return self.allocation.status

    @status.on_success()
    def _on_success_transition(self, descriptor, source, target):
        if self.allocation is None:
            return

        # TODO notify users etc.
        with transaction.atomic():
            self.allocation.save()

        allocation_status_change.send(sender=self.__class__, source=source, target=target)

    @status.transition(
        source=AllocationStatusChoices.STATUS_NEW,
        label=_("Request"),
        permission=this.can_request,
    )
    def request(self):
        pass

    @status.transition(
        source={
            AllocationStatusChoices.STATUS_NEW,
            AllocationStatusChoices.STATUS_RENEW,
        },
        target=AllocationStatusChoices.STATUS_APPROVED,
        label=_("Approve"),
    )
    def approve(self):
        pass

    @status.transition(
        source={
            AllocationStatusChoices.STATUS_NEW,
            AllocationStatusChoices.STATUS_RENEW,
        },
        target=AllocationStatusChoices.STATUS_DENIED,
        label=_("Deny"),
    )
    def deny(self):
        pass

    @status.transition(
        source={
            AllocationStatusChoices.STATUS_ACTIVE,
            AllocationStatusChoices.STATUS_EXPIRED,
            AllocationStatusChoices.STATUS_REVOKED,
            AllocationStatusChoices.STATUS_DENIED,
        },
        target=AllocationStatusChoices.STATUS_RENEW,
        label=_("Renew"),
    )
    def renew(self):
        pass

    @status.transition(
        source={
            AllocationStatusChoices.STATUS_APPROVED,
        },
        target=AllocationStatusChoices.STATUS_ACTIVE,
        label=_("Activate"),
    )
    def activate(self):
        pass

    @status.transition(
        source=AllocationStatusChoices.STATUS_ACTIVE,
        target=AllocationStatusChoices.STATUS_EXPIRED,
        label=_("Expire"),
    )
    def expire(self):
        pass

    @status.transition(
        source=AllocationStatusChoices.STATUS_ACTIVE,
        target=AllocationStatusChoices.STATUS_REVOKED,
        label=_("Revoke"),
    )
    def revoke(self):
        pass

    def can_request(self, user):
        """
        This function checks to see if the allocation can be requested. Sub-classes can override to provide custom logic
        """
        return True
