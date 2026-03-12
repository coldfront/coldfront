# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.backends import ModelBackend

from coldfront.auth.mixins import ObjectPermissionMixin


class ObjectPermissionBackend(ObjectPermissionMixin, ModelBackend):
    pass
