# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.dispatch import Signal

# Signals the allocation status has changed
allocation_status_change = Signal()
