# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.users.tables import TokenTable

from .models import UserToken


class UserTokenTable(TokenTable):
    class Meta(TokenTable.Meta):
        model = UserToken
