# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.contrib.auth.backends import ModelBackend

from coldfront.auth.mixins import ObjectPermissionMixin


class ObjectPermissionBackend(ObjectPermissionMixin, ModelBackend):
    pass
