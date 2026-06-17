# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import PrimaryModelFilterSetForm
from coldfront.forms.fields import TagFilterField
from coldfront.slurm.models import SlurmCluster, SlurmPartition


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
