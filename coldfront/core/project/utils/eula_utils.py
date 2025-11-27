# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.config.core import ALLOCATION_EULA_ENABLE
from coldfront.core.allocation.models import AllocationUserStatusChoice


def determine_eula_status_for_allocation_user(allocation, user_obj):
    """Handles EULA acceptance for allocation user if EULA is enabled for allocation."""
    allocation_user_active_status_choice = AllocationUserStatusChoice.objects.get(name="Active")

    if ALLOCATION_EULA_ENABLE:
        allocation_user_pending_status_choice = AllocationUserStatusChoice.objects.get(name="PendingEULA")
        has_eula = allocation.get_eula()
        if has_eula:
            # Logic to handle EULA acceptance can be added here
            if allocation.allocationuser_set.filter(user=user_obj).exists():
                allocation_user_obj = allocation.allocationuser_set.get(user=user_obj)
                # don't set back to pending if already active
                if allocation_user_obj.status != allocation_user_active_status_choice:
                    return allocation_user_pending_status_choice
            else:
                return allocation_user_pending_status_choice
    return allocation_user_active_status_choice
