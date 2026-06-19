# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import PrimaryModelForm, PrimaryModelImportForm, TenancyForm, TenancyImportForm
from coldfront.forms.fields import CSVModelChoiceField, JSONField
from coldfront.slurm.models import SlurmCluster, SlurmPartition


class SlurmClusterForm(TenancyForm, PrimaryModelForm):
    schema = JSONField(
        label=_("Schema"),
        required=False,
        help_text=_("Enter a valid JSON schema to define supported allocation attributes."),
    )

    class Meta:
        model = SlurmCluster
        fields = [
            "name",
            "tenant_group",
            "tenant",
            "description",
            "locked",
            "schema",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Cluster"),
                "name",
                "description",
                "locked",
                "schema",
            ),
        ]


class SlurmClusterImportForm(TenancyImportForm, PrimaryModelImportForm):
    class Meta:
        model = SlurmCluster
        fields = [
            "name",
            "tenant",
            "description",
            "locked",
            "schema",
            "tags",
        ]


class SlurmPartitionForm(PrimaryModelForm):
    cluster = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        label=_("Cluster"),
    )

    schema = JSONField(
        label=_("Schema"),
        required=False,
        help_text=_("Enter a valid JSON schema to define supported allocation attributes."),
    )

    class Meta:
        model = SlurmPartition
        fields = [
            "cluster",
            "name",
            "description",
            "locked",
            "schema",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Partition"),
                "cluster",
                "name",
                "description",
                "locked",
                "schema",
            ),
        ]


class SlurmPartitionImportForm(PrimaryModelImportForm):
    cluster = CSVModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        to_field_name="name",
        label=_("Cluster"),
    )

    class Meta:
        model = SlurmPartition
        fields = [
            "cluster",
            "name",
            "description",
            "locked",
            "schema",
            "tags",
        ]
