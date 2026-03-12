# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.config.base import AUTHENTICATION_BACKENDS, MIDDLEWARE
from coldfront.config.env import ENV

# ------------------------------------------------------------------------------
# ColdFront default authentication settings
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = "users.User"

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

SESSION_COOKIE_AGE = ENV.int("SESSION_INACTIVITY_TIMEOUT", default=60 * 60)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SECURE = True

API_TOKEN_PEPPERS = ENV.dict("API_TOKEN_PEPPERS", default={})

# ------------------------------------------------------------------------------
# The remote authentication backend to use
# ------------------------------------------------------------------------------
REMOTE_AUTH_BACKEND = ENV.str("REMOTE_AUTH_BACKEND", default="coldfront.auth.RemoteUserBackend")

# ------------------------------------------------------------------------------
# ColdFront RemoteUserBackend settings
# ------------------------------------------------------------------------------
REMOTE_AUTH_ENABLED = ENV.bool("REMOTE_AUTH_ENABLED", default=False)
REMOTE_AUTH_AUTO_CREATE_GROUPS = ENV.bool("REMOTE_AUTH_AUTO_CREATE_GROUPS", default=False)
REMOTE_AUTH_AUTO_CREATE_USER = ENV.bool("REMOTE_AUTH_AUTO_CREATE_USER", default=False)
REMOTE_AUTH_DEFAULT_GROUPS = ENV.list("REMOTE_AUTH_DEFAULT_GROUPS", default=[])
REMOTE_AUTH_DEFAULT_PERMISSIONS = ENV.dict("REMOTE_AUTH_DEFAULT_PERMISSIONS", default={})
REMOTE_AUTH_GROUP_HEADER = ENV.str("REMOTE_AUTH_GROUP_HEADER", default="HTTP_REMOTE_USER_GROUP")
REMOTE_AUTH_GROUP_SEPARATOR = ENV.str("REMOTE_AUTH_GROUP_SEPARATOR", default="|")
REMOTE_AUTH_GROUP_SYNC_ENABLED = ENV.bool("REMOTE_AUTH_GROUP_SYNC_ENABLED", default=False)
REMOTE_AUTH_HEADER = ENV.str("REMOTE_AUTH_HEADER", default="HTTP_REMOTE_USER")
REMOTE_AUTH_SUPERUSER_GROUPS = ENV.list("REMOTE_AUTH_SUPERUSER_GROUPS", default=[])
REMOTE_AUTH_SUPERUSERS = ENV.list("REMOTE_AUTH_SUPERUSERS", default=[])
REMOTE_AUTH_USER_EMAIL = ENV.str("REMOTE_AUTH_USER_EMAIL", default="HTTP_REMOTE_USER_EMAIL")
REMOTE_AUTH_USER_FIRST_NAME = ENV.str("REMOTE_AUTH_USER_FIRST_NAME", default="HTTP_REMOTE_USER_FIRST_NAME")
REMOTE_AUTH_USER_LAST_NAME = ENV.str("REMOTE_AUTH_USER_LAST_NAME", default="HTTP_REMOTE_USER_LAST_NAME")

# ------------------------------------------------------------------------------
# ColdFront LDAPBackend settings
# ------------------------------------------------------------------------------
LDAP_SEARCH_SCOPE = ENV.str("LDAP_SEARCH_SCOPE", default="onelevel")
LDAP_IGNORE_CERT_ERRORS = ENV.bool("LDAP_IGNORE_CERT_ERRORS", default=False)
LDAP_USER_SEARCH_BASE = ENV.str("LDAP_USER_SEARCH_BASE", default=None)
LDAP_USER_SEARCH_QUERY = ENV.str("LDAP_USER_SEARCH_QUERY", default="(uid=%(user)s)")
LDAP_GROUP_SEARCH_BASE = ENV.str("LDAP_GROUP_SEARCH_BASE", default=None)
LDAP_GROUP_SEARCH_QUERY = ENV.str("LDAP_GROUP_SEARCH_QUERY", default="(objectClass=groupOfNames)")
LDAP_GROUP_TYPE = ENV.str("LDAP_GROUP_TYPE", default=None)

# Expose AUTH_LDAP_* settings directly
# See: https://django-auth-ldap.readthedocs.io/en/stable/example.html
AUTH_LDAP_SERVER_URI = ENV.str("AUTH_LDAP_SERVER_URI", default=None)
AUTH_LDAP_USER_DN_TEMPLATE = ENV.str("AUTH_LDAP_USER_DN_TEMPLATE", default=None)
AUTH_LDAP_START_TLS = ENV.bool("AUTH_LDAP_START_TLS", default=False)
AUTH_LDAP_BIND_DN = ENV.str("AUTH_LDAP_BIND_DN", default=None)
AUTH_LDAP_BIND_PASSWORD = ENV.str("AUTH_LDAP_BIND_PASSWORD", default=None)
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = ENV.bool("AUTH_LDAP_BIND_AS_AUTHENTICATING_USER", default=False)
AUTH_LDAP_REQUIRE_GROUP = ENV.str("AUTH_LDAP_REQUIRE_GROUP", default=None)
AUTH_LDAP_DENY_GROUP = ENV.str("AUTH_LDAP_DENY_GROUP", default=None)
AUTH_LDAP_MIRROR_GROUPS = ENV.bool("AUTH_LDAP_MIRROR_GROUPS", default=True)
AUTH_LDAP_USER_FLAGS_BY_GROUP = ENV.dict("AUTH_LDAP_USER_FLAGS_BY_GROUP", default={})
AUTH_LDAP_USER_ATTR_MAP = ENV.dict(
    "AUTH_LDAP_USER_ATTR_MAP",
    default={
        "username": "uid",
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
    },
)

# ------------------------------------------------------------------------------
# ColdFront MokeyAuthenticationBackend settings
# ------------------------------------------------------------------------------
MOKEY_OIDC_PI_GROUP = ENV.str("MOKEY_OIDC_PI_GROUP", default="pi")
MOKEY_OIDC_ALLOWED_GROUPS = ENV.list("MOKEY_OIDC_ALLOWED_GROUPS", default=[])
MOKEY_OIDC_DENY_GROUPS = ENV.list("MOKEY_OIDC_DENY_GROUPS", default=[])

# ------------------------------------------------------------------------------
# mozilla_django_oidc settings
# ------------------------------------------------------------------------------
OIDC_OP_JWKS_ENDPOINT = ENV.str("OIDC_OP_JWKS_ENDPOINT", default=None)
OIDC_RP_SIGN_ALGO = ENV.str("OIDC_RP_SIGN_ALGO", default=None)
OIDC_RP_CLIENT_ID = ENV.str("OIDC_RP_CLIENT_ID", default=None)
OIDC_RP_CLIENT_SECRET = ENV.str("OIDC_RP_CLIENT_SECRET", default=None)
OIDC_OP_AUTHORIZATION_ENDPOINT = ENV.str("OIDC_OP_AUTHORIZATION_ENDPOINT", default=None)
OIDC_OP_TOKEN_ENDPOINT = ENV.str("OIDC_OP_TOKEN_ENDPOINT", default=None)
OIDC_OP_USER_ENDPOINT = ENV.str("OIDC_OP_USER_ENDPOINT", default=None)
OIDC_VERIFY_SSL = ENV.bool("OIDC_VERIFY_SSL", default=True)
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = ENV.int("OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS", default=3600)
OIDC_ENABLE_SESSION_REFRESH = ENV.bool("OIDC_ENABLE_SESSION_REFRESH", default=False)

if type(REMOTE_AUTH_BACKEND) not in (list, tuple):
    REMOTE_AUTH_BACKEND = [REMOTE_AUTH_BACKEND]

AUTHENTICATION_BACKENDS += [
    *REMOTE_AUTH_BACKEND,
    "coldfront.auth.backends.ObjectPermissionBackend",
]

if OIDC_ENABLE_SESSION_REFRESH:
    MIDDLEWARE += [
        "mozilla_django_oidc.middleware.SessionRefresh",
    ]
