# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from coldfront.registry import registry


def get_table_for_model(model, name=None):
    name = name or f"{model.__name__}Table"
    try:
        return import_string(f"{model._meta.app_label}.tables.{name}")
    except ImportError:
        return None


def register_table_column(column, name, *tables):
    """
    Register a custom column for use on one or more tables.

    Args:
        column: The column instance to register
        name: The name of the table column
        tables: One or more table classes
    """
    for table in tables:
        reg = registry["tables"][table]
        if name in reg:
            raise ValueError(
                _("A column named {name} is already defined for table {table_name}").format(
                    name=name, table_name=table.__name__
                )
            )
        reg[name] = column
