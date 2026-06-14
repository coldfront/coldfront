# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from generic_notifications.channels import WebsiteChannel
from generic_notifications.frequencies import RealtimeFrequency
from generic_notifications.types import NotificationType, register


class ColdFrontNotification(NotificationType):
    default_frequency = RealtimeFrequency
    default_channels = [WebsiteChannel]


@register
class SystemMessage(ColdFrontNotification):
    key = "system_message"
    name = "System Message"
    description = "Important system notifications"

    def get_subject(self, notification):
        """Generate subject for system messages."""
        if notification.subject:
            return notification.subject
        return f"System Message: {self.name}"

    def get_text(self, notification):
        """Generate text for system messages."""
        if notification.text:
            return notification.text
        return self.description or f"You have a new {self.name.lower()} notification"
