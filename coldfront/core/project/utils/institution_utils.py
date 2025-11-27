# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.conf import settings


def determine_automated_institution_choice(project, institution_map: dict):
    """
    Determine automated institution choice for a project. Taking PI email of current project
    and comparing to domain key from institution_map. Will first try to match a domain exactly
    as provided in institution_map, if a direct match cannot be found an indirect match will be
    attempted by looking for the first occurrence of an institution domain that occurs as a substring
    in the PI's email address. This does not save changes to the database. The project object in
    memory will have the institution field modified.
    :param project: Project to add automated institution choice to.
    :param institution_map: Dictionary of institution keys, values.
    """
    email: str = project.pi.email

    try:
        _, pi_email_domain = email.split("@")
    except ValueError:
        pi_email_domain = None

    direct_institution_match = institution_map.get(pi_email_domain)

    if direct_institution_match:
        project.institution = direct_institution_match
        return direct_institution_match
    else:
        for institution_email_domain, indirect_institution_match in institution_map.items():
            if institution_email_domain in pi_email_domain:
                project.institution = indirect_institution_match
                return indirect_institution_match

    return project.institution


def add_institution(project_obj):
    """
    Add automated institution choice to project if feature is enabled.
    :param project_obj: Project object to add institution choice to.
    """
    if hasattr(settings, "PROJECT_INSTITUTION_EMAIL_MAP"):
        determine_automated_institution_choice(project_obj, settings.PROJECT_INSTITUTION_EMAIL_MAP)
