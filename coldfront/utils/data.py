# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0
import datetime

from django.utils import timezone
from django.utils.timezone import localtime

__all__ = (
    "get_config_value_ci",
    "shallow_compare_dict",
)


def get_config_value_ci(config_dict, key, default=None):
    """
    Retrieve a value from a dictionary using case-insensitive key matching.
    """
    if key in config_dict:
        return config_dict[key]
    key_lower = key.lower()
    for config_key, value in config_dict.items():
        if config_key.lower() == key_lower:
            return value
    return default


def shallow_compare_dict(source_dict, destination_dict, exclude=tuple()):
    """
    Return a new dictionary of the different keys. The values of `destination_dict` are returned. Only the equality of
    the first layer of keys/values is checked. `exclude` is a list or tuple of keys to be ignored.
    """
    difference = {}

    for key, value in destination_dict.items():
        if key in exclude:
            continue
        if source_dict.get(key) != value:
            difference[key] = value

    return difference


def local_now():
    """
    Return the current date & time in the system timezone.
    """
    return localtime(timezone.now())


def datetime_from_timestamp(value):
    """
    Convert an ISO 8601 or RFC 3339 timestamp to a datetime object.
    """
    return datetime.datetime.fromisoformat(value)
