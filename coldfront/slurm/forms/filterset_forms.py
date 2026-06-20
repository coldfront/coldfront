# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import PrimaryModelFilterSetForm
from coldfront.forms.fields import TagFilterField
from coldfront.slurm.models import SlurmAccount, SlurmAssociation, SlurmCluster, SlurmPartition, SlurmQOS, SlurmUser


class SlurmQOSFilterSetForm(PrimaryModelFilterSetForm):
    model = SlurmQOS
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Slurm QOS"),
            "tag",
        ),
    )


class SlurmClusterFilterSetForm(PrimaryModelFilterSetForm):
    model = SlurmCluster
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Slurm Cluster"),
            "tag",
        ),
    )


class SlurmPartitionFilterSetForm(PrimaryModelFilterSetForm):
    model = SlurmPartition
    cluster_id = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Slurm Partition"),
            "cluster_id",
            "tag",
        ),
    )


class SlurmAccountFilterSetForm(PrimaryModelFilterSetForm):
    model = SlurmAccount
    cluster_id = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Slurm Account"),
            "cluster_id",
            "tag",
        ),
    )


class SlurmAssociationFilterSetForm(PrimaryModelFilterSetForm):
    model = SlurmAssociation
    slurm_account_id = forms.ModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        required=False,
        label=_("Slurm Account"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Slurm Association"),
            "slurm_account_id",
            "tag",
        ),
    )


class SlurmUserFilterSetForm(PrimaryModelFilterSetForm):
    model = SlurmUser
    cluster_id = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Slurm User"),
            "cluster_id",
            "tag",
        ),
    )
