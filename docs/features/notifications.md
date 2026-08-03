# Notifications

ColdFront uses `django-generic-notifications` to send notifications to
users when allocation status changes occur. Notifications appear in the
web interface and can be configured by each user.

## Notification Types

ColdFront defines a `ColdFrontNotification` base type with two
notification types:

- **AllocationsNotificationType** — Sent when an allocation is approved.
  The allocation owner receives a notification with the allocation slug,
  project name, and a link to the allocation detail page.
- **SystemMessage** — Used for important system notifications. Sent to
  superusers and any users or groups configured in the system settings.

## How Notifications Work

Notifications are sent automatically by the allocation workflow. When an
allocation transitions to the approved status, the flow calls
`send_notification` with the allocation owner as the recipient.

System notifications can be sent programmatically using the
`send_system_notification` function. Recipients include:

- All superusers (always included)
- Users listed in `SYSTEM_NOTIFICATION_USERS` setting
- Members of groups listed in `SYSTEM_NOTIFICATION_GROUPS` setting

## User Configuration

Users can configure their notification preferences in the user interface.
They can choose which notification types to receive and how frequently
to receive them. Notifications are displayed in the web interface and
can be marked as read or deleted.

!!! warning "Work in progress"

    The notification system is still under development. Some features
    may not be fully available.
