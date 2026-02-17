# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.utils.translation import gettext_lazy as _

from coldfront.utils.choices import ChoiceSet


class ObjectChangeActionChoices(ChoiceSet):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"

    CHOICES = (
        (ACTION_CREATE, _("Created"), "green"),
        (ACTION_UPDATE, _("Updated"), "blue"),
        (ACTION_DELETE, _("Deleted"), "red"),
    )
