# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.users.tables import TokenTable

from .models import UserToken


class UserTokenTable(TokenTable):
    class Meta(TokenTable.Meta):
        model = UserToken
