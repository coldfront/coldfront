# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from coldfront.choices import ChoiceSet
from coldfront.core.models import ObjectType
from coldfront.utils.forms import add_blank_choice


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

    CHOICES = [
        (STATUS_ARCHIVED, _("Archived"), "secondary"),
        (STATUS_ACTIVE, _("Active"), "success"),
    ]


class AllocationStatusChoices(ChoiceSet):
    key = "Allocation.status"

    STATUS_NEW = "new"
    STATUS_ACTIVE = "active"
    STATUS_DENIED = "denied"
    STATUS_EXPIRED = "expired"
    STATUS_APPROVED = "approved"
    STATUS_REVOKED = "revoked"
    STATUS_RENEW = "renew"

    CHOICES = [
        (STATUS_NEW, _("New"), "info"),
        (STATUS_ACTIVE, _("Active"), "success"),
        (STATUS_DENIED, _("Denied"), "danger"),
        (STATUS_EXPIRED, _("Expired"), "warning"),
        (STATUS_APPROVED, _("Approved"), "primary"),
        (STATUS_REVOKED, _("Revoked"), "danger"),
        (STATUS_RENEW, _("Renew"), "info"),
    ]


def get_resource_object_choices():
    """
    Build a list of optgroup choices for all objects with the "allocatable_resource" feature.
    Returns a list of (optgroup_label, [(value, label), ...]) tuples.
    """
    choices = []
    for ot in ObjectType.objects.with_feature("allocatable_resource").order_by("app_label", "model"):
        model_class = ot.model_class()
        if model_class is None:
            continue
        ct = ContentType.objects.get_for_model(model_class)
        model_choices = []
        for obj in model_class.objects.all():
            if not obj.is_allocatable:
                continue
            value = f"{ct.id}:{obj.id}"
            label = str(obj)
            model_choices.append((value, label))
        optgroup_label = model_class._meta.verbose_name_plural.title()
        choices.append((optgroup_label, model_choices))
    return add_blank_choice(choices)
