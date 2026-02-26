# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.utils.translation import gettext_lazy as _

from coldfront.utils.choices import ChoiceSet


class ResourceStatusChoices(ChoiceSet):
    key = "Resource.status"

    STATUS_OFFLINE = "offline"
    STATUS_ACTIVE = "active"
    STATUS_PLANNED = "planned"
    STATUS_STAGED = "staged"
    STATUS_DECOMMISSIONING = "decommissioning"

    CHOICES = [
        (STATUS_OFFLINE, _("Offline"), "secondary"),
        (STATUS_ACTIVE, _("Active"), "success"),
        (STATUS_PLANNED, _("Planned"), "danger"),
        (STATUS_STAGED, _("Staged"), "info"),
        (STATUS_DECOMMISSIONING, _("Decommissioning"), "warning"),
    ]


class ProjectStatusChoices(ChoiceSet):
    key = "Project.status"

    STATUS_ARCHIVED = "archived"
    STATUS_ACTIVE = "active"
    STATUS_NEW = "new"

    CHOICES = [
        (STATUS_ARCHIVED, _("Archived"), "secondary"),
        (STATUS_ACTIVE, _("Active"), "success"),
        (STATUS_NEW, _("New"), "info"),
    ]


class AllocationStatusChoices(ChoiceSet):
    key = "Allocation.status"

    STATUS_ACTIVE = "active"
    STATUS_NEW = "new"
    STATUS_DENIED = "denied"
    STATUS_EXPIRED = "expired"

    CHOICES = [
        (STATUS_EXPIRED, _("Expired"), "warning"),
        (STATUS_ACTIVE, _("Active"), "success"),
        (STATUS_NEW, _("New"), "info"),
        (STATUS_DENIED, _("Denied"), "danger"),
    ]
