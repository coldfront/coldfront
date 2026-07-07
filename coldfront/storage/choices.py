# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from coldfront.choices import ChoiceSet


class StorageShareTypeChoices(ChoiceSet):
    key = "StorageQuota.share_type"

    SHARE_TYPE_POSIX = "posix"
    SHARE_TYPE_SMB = "smb"
    SHARE_TYPE_NFS = "nfs"

    CHOICES = [
        (SHARE_TYPE_POSIX, _("POSIX"), "info"),
        (SHARE_TYPE_SMB, _("SMB"), "primary"),
        (SHARE_TYPE_NFS, _("NFS"), "success"),
    ]
