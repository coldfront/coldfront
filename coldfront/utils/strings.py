# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0


def title(value):
    """
    Improved implementation of str.title(); retains all existing uppercase letters.
    """
    return " ".join([w[0].upper() + w[1:] for w in str(value).split()])
