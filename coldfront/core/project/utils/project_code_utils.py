# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.conf import settings


def generate_project_code(project_code: str, project_pk: int, padding: int = 0) -> str:
    """
    Generate a formatted project code by combining an uppercased user-defined project code,
    project primary key and requested padding value (default = 0).

    :param project_code: The base project code, set through the PROJECT_CODE configuration variable.
    :param project_pk: The primary key of the project.
    :param padding: The number of digits to pad the primary key with, set through the PROJECT_CODE_PADDING configuration variable.
    :return: A formatted project code string.
    """

    return f"{project_code.upper()}{str(project_pk).zfill(padding)}"


def add_project_code_if_missing(project_obj):
    """Updates project code if no value was set, providing the feature is activated."""
    project_code = getattr(settings, "PROJECT_CODE", False)
    if project_code and project_obj.project_code == "":
        pc_padding = getattr(settings, "PROJECT_CODE_PADDING", False) or 0
        project_obj.project_code = generate_project_code(project_code, project_obj.pk, pc_padding)
        project_obj.save(update_fields=["project_code"])
