# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


def add_project_status_choices(apps, schema_editor):
    ProjectStatusChoice = apps.get_model("project", "ProjectStatusChoice")

    for choice in [
        "New",
        "Active",
        "Archived",
    ]:
        ProjectStatusChoice.objects.get_or_create(name=choice)


def add_project_user_role_choices(apps, schema_editor):
    ProjectUserRoleChoice = apps.get_model("project", "ProjectUserRoleChoice")

    for choice in [
        "User",
        "Manager",
    ]:
        ProjectUserRoleChoice.objects.get_or_create(name=choice)


def add_project_user_status_choices(apps, schema_editor):
    ProjectUserStatusChoice = apps.get_model("project", "ProjectUserStatusChoice")

    for choice in [
        "Active",
        "Pending Remove",
        "Denied",
        "Removed",
    ]:
        ProjectUserStatusChoice.objects.get_or_create(name=choice)


def project_is_archived(project_obj):
    """Utility function to check if a project is archived."""
    return project_obj.status.name not in ["Active", "New"]


def get_project_attributes(project_obj, show_private=False):
    """Utility function to get project attributes."""
    if show_private:
        return project_obj.projectattribute_set.all().order_by("proj_attr_type__name")
    else:
        return project_obj.projectattribute_set.filter(proj_attr_type__is_private=False).order_by(
            "proj_attr_type__name"
        )
