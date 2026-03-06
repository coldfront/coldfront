# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.config.base import AUTHENTICATION_BACKENDS
from coldfront.config.env import ENV

# ------------------------------------------------------------------------------
# ColdFront default authentication settings
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS += [
    "django.contrib.auth.backends.ModelBackend",
    "coldfront.auth.backends.ObjectPermissionBackend",
]

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = ENV.str("LOGOUT_REDIRECT_URL", LOGIN_URL)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SU_LOGIN_CALLBACK = "coldfront.legacy.utils.common.su_login_callback"
SU_LOGOUT_REDIRECT_URL = "/admin/auth/user/"

SESSION_COOKIE_AGE = ENV.int("SESSION_INACTIVITY_TIMEOUT", default=60 * 60)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SECURE = True
