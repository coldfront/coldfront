# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django.utils.translation import gettext_lazy as _

from coldfront.forms import (
    OrganizationalModelForm,
    PrimaryModelForm,
    PrimaryModelImportForm,
    TenancyForm,
    TenancyImportForm,
)
from coldfront.forms.fields import CSVModelChoiceField, DynamicModelChoiceField
from coldfront.ras.models import Project, ProjectUser
from coldfront.users.models import User


class ProjectForm(TenancyForm, OrganizationalModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "status",
            "description",
            "tags",
            "tenant",
            "tenant_group",
        ]

    fieldsets = (
        Fieldset(
            _("Project"),
            "name",
            "status",
            "description",
        ),
    )


class ProjectUserForm(PrimaryModelForm):
    user = DynamicModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
        selector=True,
        context={
            "label": "username",
            "title": "Username,First Name,Last Name,Email",
            "extra-columns": "first_name,last_name,email",
        },
    )

    class Meta:
        model = ProjectUser
        fields = [
            "project",
            "user",
        ]

    fieldsets = (
        Fieldset(
            _("Project User"),
            "project",
            "user",
        ),
    )


class ProjectImportForm(TenancyImportForm, PrimaryModelImportForm):
    owner = CSVModelChoiceField(
        label=_("Owner"),
        queryset=User.objects.all(),
        required=True,
        to_field_name="username",
        help_text=_("Owner of the project"),
        error_messages={
            "invalid_choice": _("User not found."),
        },
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "owner",
            "status",
            "description",
            "tags",
            "tenant",
            "tenant_group",
        ]


class ProjectUserImportForm(PrimaryModelImportForm):
    user = CSVModelChoiceField(
        label=_("User"),
        queryset=User.objects.all(),
        required=True,
        to_field_name="username",
        help_text=_("User to add to project"),
        error_messages={
            "invalid_choice": _("User not found."),
        },
    )

    project = CSVModelChoiceField(
        label=_("Project"),
        queryset=Project.objects.all(),
        required=True,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Project not found."),
        },
    )

    class Meta:
        model = ProjectUser
        fields = [
            "user",
            "project",
        ]
