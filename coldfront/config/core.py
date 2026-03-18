# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import coldfront
from coldfront.config.base import SETTINGS_EXPORT
from coldfront.config.env import ENV

# ------------------------------------------------------------------------------
# Advanced ColdFront configurations
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# General Center Information
# ------------------------------------------------------------------------------
CENTER_NAME = ENV.str("CENTER_NAME", default="HPC Center")
CENTER_HELP_URL = ENV.str("CENTER_HELP_URL", default="")
CENTER_PROJECT_RENEWAL_HELP_URL = ENV.str("CENTER_PROJECT_RENEWAL_HELP_URL", default="")
CENTER_BASE_URL = ENV.str("CENTER_BASE_URL", default="")

# ------------------------------------------------------------------------------
# Enable Research Outputs, Grants, Publications
# ------------------------------------------------------------------------------
RESEARCH_OUTPUT_ENABLE = ENV.bool("RESEARCH_OUTPUT_ENABLE", default=True)
GRANT_ENABLE = ENV.bool("GRANT_ENABLE", default=True)
PUBLICATION_ENABLE = ENV.bool("PUBLICATION_ENABLE", default=True)

# ------------------------------------------------------------------------------
# Enable Project Review
# ------------------------------------------------------------------------------
PROJECT_ENABLE_PROJECT_REVIEW = ENV.bool("PROJECT_ENABLE_PROJECT_REVIEW", default=True)

# ------------------------------------------------------------------------------
# Enable EULA force agreement
# ------------------------------------------------------------------------------
ALLOCATION_EULA_ENABLE = ENV.bool("ALLOCATION_EULA_ENABLE", default=False)

# ------------------------------------------------------------------------------
# Allocation related
# ------------------------------------------------------------------------------
ALLOCATION_ENABLE_CHANGE_REQUESTS_BY_DEFAULT = ENV.bool("ALLOCATION_ENABLE_CHANGE_REQUESTS", default=True)
ALLOCATION_CHANGE_REQUEST_EXTENSION_DAYS = ENV.list(
    "ALLOCATION_CHANGE_REQUEST_EXTENSION_DAYS", cast=int, default=[30, 60, 90]
)
ALLOCATION_ENABLE_ALLOCATION_RENEWAL = ENV.bool("ALLOCATION_ENABLE_ALLOCATION_RENEWAL", default=True)
ALLOCATION_FUNCS_ON_EXPIRE = [
    "coldfront.legacy.allocation.utils.test_allocation_function",
]

# This is in days
ALLOCATION_DEFAULT_ALLOCATION_LENGTH = ENV.int("ALLOCATION_DEFAULT_ALLOCATION_LENGTH", default=365)

# ------------------------------------------------------------------------------
# Allow user to select account name for allocation
# ------------------------------------------------------------------------------
ALLOCATION_ACCOUNT_ENABLED = ENV.bool("ALLOCATION_ACCOUNT_ENABLED", default=False)
ALLOCATION_ACCOUNT_MAPPING = ENV.dict("ALLOCATION_ACCOUNT_MAPPING", default={})

SETTINGS_EXPORT += [
    "ALLOCATION_ACCOUNT_ENABLED",
    "ALLOCATION_DEFAULT_ALLOCATION_LENGTH",
    "ALLOCATION_ENABLE_ALLOCATION_RENEWAL",
    "ALLOCATION_EULA_ENABLE",
    "CENTER_HELP_URL",
    "GRANT_ENABLE",
    "INVOICE_ENABLED",
    "PROJECT_ENABLE_PROJECT_REVIEW",
    "PROJECT_INSTITUTION_EMAIL_MAP",
    "PUBLICATION_ENABLE",
    "RESEARCH_OUTPUT_ENABLE",
    "DJANGO_VITE",
]

ADMIN_COMMENTS_SHOW_EMPTY = ENV.bool("ADMIN_COMMENTS_SHOW_EMPTY", default=True)

# ------------------------------------------------------------------------------
# List of Allocation Attributes to display on view page
# ------------------------------------------------------------------------------
ALLOCATION_ATTRIBUTE_VIEW_LIST = ENV.list(
    "ALLOCATION_ATTRIBUTE_VIEW_LIST",
    default=[
        "slurm_account_name",
        "freeipa_group",
        "Cloud Account Name",
    ],
)

# ------------------------------------------------------------------------------
# Enable invoice functionality
# ------------------------------------------------------------------------------
INVOICE_ENABLED = ENV.bool("INVOICE_ENABLED", default=True)
# Override default 'Pending Payment' status
INVOICE_DEFAULT_STATUS = ENV.str("INVOICE_DEFAULT_STATUS", default="New")

# ------------------------------------------------------------------------------
# Enable Open OnDemand integration
# ------------------------------------------------------------------------------
ONDEMAND_URL = ENV.str("ONDEMAND_URL", default=None)

# ------------------------------------------------------------------------------
# Default Strings. Override these in local_settings.py
# ------------------------------------------------------------------------------
LOGIN_FAIL_MESSAGE = ENV.str("LOGIN_FAIL_MESSAGE", "")

EMAIL_DIRECTOR_PENDING_PROJECT_REVIEW_EMAIL = """
You recently applied for renewal of your account, however, to date you have not entered any publication nor grant info in the ColdFront system. I am reluctant to approve your renewal without understanding why. If there are no relevant publications or grants yet, then please let me know. If there are, then I would appreciate it if you would take the time to enter the data (I have done it myself and it took about 15 minutes). We use this information to help make the case to the university for continued investment in our department and it is therefore important that faculty enter the data when appropriate. Please email xxx-helpexample.com if you need technical assistance.

As always, I am available to discuss any of this.

Best regards
Director


xxx@example.edu
Phone: (xxx) xxx-xxx
"""

ACCOUNT_CREATION_TEXT = """University faculty can submit a help ticket to request an account.
Please see <a href="#">instructions on our website</a>. Staff, students, and external collaborators must
request an account through a university faculty member.
"""


# ------------------------------------------------------------------------------
# Provide institution project code.
# ------------------------------------------------------------------------------

PROJECT_CODE = ENV.str("PROJECT_CODE", default=None)
PROJECT_CODE_PADDING = ENV.int("PROJECT_CODE_PADDING", default=None)

# ------------------------------------------------------------------------------
# Enable project institution code feature.
# ------------------------------------------------------------------------------

PROJECT_INSTITUTION_EMAIL_MAP = ENV.dict("PROJECT_INSTITUTION_EMAIL_MAP", default={})

# ------------------------------------------------------------------------------
# Configure Project fields that project managers can update
# ------------------------------------------------------------------------------

PROJECT_UPDATE_FIELDS = ENV.list(
    "PROJECT_UPDATE_FIELDS",
    default=[
        "title",
        "description",
        "field_of_science",
    ],
)

EXEMPT_VIEW_PERMISSIONS = []
CHANGELOG_SKIP_EMPTY_CHANGES = True
PAGINATE_COUNT = ENV.int("PAGINATE_COUNT", default=50)
MAX_PAGE_SIZE = ENV.int("MAX_PAGE_SIZE", default=1000)
FILTERS_NULL_CHOICE_LABEL = "None"
FILTERS_NULL_CHOICE_VALUE = "null"
FIELD_CHOICES = {}
AUTO_SLUG_PREFIX = ENV.str("AUTO_SLUG_PREFIX", default="CF-")
AUTO_SLUG_FUNC = ENV.str("AUTO_SLUG_FUNC", default="")

DEFAULT_PERMISSIONS = ENV.dict(
    "DEFAULT_PERMISSIONS",
    default={
        # Permit users to manage their own API tokens
        "users.view_token": ({"user": "$user"},),
        "users.add_token": ({"user": "$user"},),
        "users.change_token": ({"user": "$user"},),
        "users.delete_token": ({"user": "$user"},),
    },
)

# Exclude potentially sensitive models from wildcard view exemption. These may still be exempted
# by specifying the model individually in the EXEMPT_VIEW_PERMISSIONS configuration parameter.
EXEMPT_EXCLUDE_MODELS = (
    ("users", "group"),
    ("users", "objectpermission"),
    ("users", "user"),
)

ALLOWED_URL_SCHEMES = [
    "file",
    "ftp",
    "ftps",
    "http",
    "https",
    "irc",
    "mailto",
    "sftp",
    "ssh",
    "tel",
    "telnet",
    "tftp",
    "vnc",
    "xmpp",
]

REST_FRAMEWORK_VERSION = coldfront.VERSION
REST_FRAMEWORK = {
    "ALLOWED_VERSIONS": [REST_FRAMEWORK_VERSION],
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "coldfront.api.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_METADATA_CLASS": "coldfront.api.metadata.BulkOperationMetadata",
    "DEFAULT_PAGINATION_CLASS": "coldfront.api.paginator.OptionalLimitOffsetPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("coldfront.api.authentication.TokenPermissions",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "coldfront.api.renderers.FormlessBrowsableAPIRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSION": REST_FRAMEWORK_VERSION,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "SCHEMA_COERCE_METHOD_NAMES": {
        # Default mappings
        "retrieve": "read",
        "destroy": "delete",
        # Custom operations
        #        'bulk_destroy': 'bulk_delete',
    },
    "VIEW_NAME_FUNCTION": "coldfront.api.utils.get_view_name",
}

#
# DRF Spectacular
#

SPECTACULAR_SETTINGS = {
    "TITLE": "ColdFront REST API",
    "LICENSE": {"name": "Apache 2.0"},
    "VERSION": coldfront.VERSION,
    "COMPONENT_SPLIT_REQUEST": True,
    "REDOC_DIST": "SIDECAR",
    "SERVERS": [
        {
            "url": "",
            "description": "ColdFront",
        }
    ],
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "POSTPROCESSING_HOOKS": [],
}
