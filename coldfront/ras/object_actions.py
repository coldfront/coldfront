# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from coldfront.views.object_actions import ObjectAction


class RequestAllocation(ObjectAction):
    """
    Request an allocation.
    """

    name = "request"
    label = _("Request")
    multi = False
    transition = "request"
    url_kwargs = ["pk"]
    permissions_required = {"request"}
    template_name = "button.request"


class ApproveAllocation(ObjectAction):
    """
    Approve an allocation.
    """

    name = "approve"
    label = _("Approve")
    multi = False
    transition = "approve"
    url_kwargs = ["pk"]
    permissions_required = {"approve"}
    template_name = "button.approve"


class DenyAllocation(ObjectAction):
    """
    Deny an allocation.
    """

    name = "deny"
    label = _("Deny")
    multi = False
    transition = "deny"
    url_kwargs = ["pk"]
    permissions_required = {"deny"}
    template_name = "button.deny"


class ActivateAllocation(ObjectAction):
    """
    Activate an allocation.
    """

    name = "activate"
    label = _("Activate")
    multi = False
    transition = "activate"
    url_kwargs = ["pk"]
    permissions_required = {"activate"}
    template_name = "button.activate"


class RenewAllocation(ObjectAction):
    """
    Renew an allocation.
    """

    name = "renew"
    label = _("Renew")
    multi = False
    transition = "renew"
    url_kwargs = ["pk"]
    permissions_required = {"renew"}
    template_name = "button.renew"


class RevokeAllocation(ObjectAction):
    """
    Revoke an allocation.
    """

    name = "revoke"
    label = _("Revoke")
    multi = False
    transition = "revoke"
    url_kwargs = ["pk"]
    permissions_required = {"revoke"}
    template_name = "button.revoke"
