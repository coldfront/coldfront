# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib.auth.backends import ModelBackend

from .mixins import ObjectPermissionMixin


class ObjectPermissionBackend(ObjectPermissionMixin, ModelBackend):
    pass
