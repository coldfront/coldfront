# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django.utils.translation import gettext_lazy as _

from coldfront.forms import OrganizationalModelForm, PrimaryModelForm
from coldfront.ras.models import Project, ProjectUser
from coldfront.tenancy.forms import TenancyForm


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
            "tags",
        ),
        Fieldset(
            _("Tenant"),
            "tenant_group",
            "tenant",
        ),
    )


class ProjectUserForm(PrimaryModelForm):
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
