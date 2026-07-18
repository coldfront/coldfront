# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import (
    AllocatableResourceBulkEditForm,
    OrganizationalModelBulkEditForm,
    PrimaryModelBulkEditForm,
)
from coldfront.forms.fields import JSONField
from coldfront.forms.widgets import BulkEditNullBooleanSelect
from coldfront.slurm.models import SlurmAccount, SlurmAssociation, SlurmCluster, SlurmPartition, SlurmQOS, SlurmUser
from coldfront.users.models.users import Group

#
# Slurm QOS
#


class SlurmQOSBulkEditForm(OrganizationalModelBulkEditForm):
    model = SlurmQOS
    nullable_fields = ("description",)

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm QOS"),
                "description",
            ),
        ]


#
# Slurm clusters
#


class SlurmClusterBulkEditForm(AllocatableResourceBulkEditForm, PrimaryModelBulkEditForm):
    default_qos = forms.ModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("Default QOS"),
    )
    qos_list = forms.ModelMultipleChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("QOS List"),
    )
    fairshare = forms.IntegerField(
        required=False,
        label=_("Fairshare"),
    )
    features = JSONField(
        label=_("Features"),
        required=False,
        help_text=_("Enter valid JSON."),
    )
    classification = forms.CharField(
        max_length=50,
        required=False,
        label=_("Classification"),
    )

    model = SlurmCluster
    nullable_fields = (
        "tenant_group",
        "tenant",
        "description",
        "locked",
        "schema",
        "default_qos",
        "qos_list",
        "fairshare",
        "features",
        "classification",
    )

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Cluster"),
                "description",
                "locked",
                "schema",
            ),
            Fieldset(
                _("Slurm Accounting"),
                "default_qos",
                "qos_list",
                "fairshare",
                "features",
                "classification",
            ),
        ]


#
# Slurm partitions
#


class SlurmPartitionBulkEditForm(AllocatableResourceBulkEditForm, PrimaryModelBulkEditForm):
    cluster = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    nodes = forms.CharField(
        max_length=255,
        required=False,
        label=_("Nodes"),
    )
    priority = forms.IntegerField(
        required=False,
        label=_("Priority"),
    )
    locked = forms.NullBooleanField(
        label=_("Locked"),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )
    is_default = forms.NullBooleanField(
        label=_("Default"),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )
    default_time = forms.IntegerField(
        required=False,
        label=_("Default Time (minutes)"),
        help_text=_("Duration in minutes"),
    )
    state = forms.CharField(
        max_length=20,
        required=False,
        label=_("State"),
    )
    preempt_mode = forms.CharField(
        max_length=20,
        required=False,
        label=_("Preempt Mode"),
    )
    def_mem_per_cpu = forms.IntegerField(
        required=False,
        label=_("Default Memory per CPU"),
    )
    max_jobs = forms.IntegerField(
        required=False,
        label=_("Max Jobs"),
    )
    max_submit_jobs = forms.IntegerField(
        required=False,
        label=_("Max Submit Jobs"),
    )
    max_tres_per_job = JSONField(
        label=_("Max TRES per Job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )
    max_tres_per_node = JSONField(
        label=_("Max TRES per Node"),
        required=False,
        help_text=_("Enter valid JSON."),
    )
    max_tres_mins_per_job = JSONField(
        label=_("Max TRES Minutes per Job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )
    max_wall_duration_per_job = forms.IntegerField(
        required=False,
        label=_("Max Wall Duration per Job (minutes)"),
        help_text=_("Duration in minutes"),
    )
    fairshare = forms.IntegerField(
        required=False,
        label=_("Fairshare"),
    )
    qos_list = forms.ModelMultipleChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("QOS List"),
    )
    allow_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label=_("Allowed Groups"),
    )
    allow_accounts = forms.ModelMultipleChoiceField(
        queryset=SlurmAccount.objects.all(),
        required=False,
        label=_("Allowed Accounts"),
    )

    model = SlurmPartition
    nullable_fields = (
        "description",
        "locked",
        "schema",
        "nodes",
        "priority",
        "is_default",
        "default_time",
        "state",
        "preempt_mode",
        "def_mem_per_cpu",
        "max_jobs",
        "max_submit_jobs",
        "max_tres_per_job",
        "max_tres_per_node",
        "max_tres_mins_per_job",
        "max_wall_duration_per_job",
        "fairshare",
        "qos_list",
        "allow_groups",
        "allow_accounts",
    )

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Partition"),
                "cluster",
                "description",
                "locked",
                "schema",
                "nodes",
                "priority",
                "is_default",
                "default_time",
                "state",
                "preempt_mode",
                "def_mem_per_cpu",
            ),
            Fieldset(
                _("Limits"),
                "max_jobs",
                "max_submit_jobs",
                "max_tres_per_job",
                "max_tres_per_node",
                "max_tres_mins_per_job",
                "max_wall_duration_per_job",
                "fairshare",
            ),
            Fieldset(
                _("Access Control"),
                "qos_list",
                "allow_groups",
                "allow_accounts",
            ),
        ]


#
# Slurm accounts
#


class SlurmAccountBulkEditForm(PrimaryModelBulkEditForm):
    cluster = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    fairshare = forms.IntegerField(
        required=False,
        label=_("Fairshare"),
    )
    qos_list = forms.ModelMultipleChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("QOS List"),
    )

    model = SlurmAccount
    nullable_fields = ("description", "fairshare", "qos_list")

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Account"),
                "cluster",
                "description",
                "fairshare",
                "qos_list",
            ),
        ]


#
# Slurm associations
#


class SlurmAssociationBulkEditForm(PrimaryModelBulkEditForm):
    slurm_account = forms.ModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        required=False,
        label=_("Slurm Account"),
    )
    parent = forms.ModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        required=False,
        label=_("Parent Account"),
    )
    default_qos = forms.ModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("Default QOS"),
    )
    fairshare = forms.IntegerField(
        required=False,
        label=_("Fairshare"),
    )
    max_jobs = forms.IntegerField(
        required=False,
        label=_("Max Jobs"),
    )
    max_submit_jobs = forms.IntegerField(
        required=False,
        label=_("Max Submit Jobs"),
    )
    max_tres_per_job = JSONField(
        label=_("Max TRES per Job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )
    max_tres_mins_per_job = JSONField(
        label=_("Max TRES Minutes per Job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )
    max_wall_duration_per_job = forms.IntegerField(
        required=False,
        label=_("Max Wall Duration per Job (minutes)"),
        help_text=_("Duration in minutes"),
    )

    model = SlurmAssociation
    nullable_fields = (
        "description",
        "slurm_account",
        "parent",
        "default_qos",
        "fairshare",
        "max_jobs",
        "max_submit_jobs",
        "max_tres_per_job",
        "max_tres_mins_per_job",
        "max_wall_duration_per_job",
    )

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Association"),
                "slurm_account",
                "parent",
                "default_qos",
                "fairshare",
            ),
            Fieldset(
                _("Limits"),
                "max_jobs",
                "max_submit_jobs",
                "max_tres_per_job",
                "max_tres_mins_per_job",
                "max_wall_duration_per_job",
            ),
        ]


#
# Slurm users
#


class SlurmUserBulkEditForm(PrimaryModelBulkEditForm):
    cluster = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    default_account = forms.ModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        required=False,
        label=_("Default Account"),
    )
    default_wckey = forms.CharField(
        max_length=100,
        required=False,
        label=_("Default WCKey"),
    )
    default_qos = forms.ModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("Default QOS"),
    )
    admin_level = forms.IntegerField(
        required=False,
        label=_("Admin Level"),
        widget=forms.Select(
            choices=[
                ("", _("---------")),
                (0, _("None")),
                (1, _("Operator")),
                (2, _("Admin")),
            ]
        ),
    )

    model = SlurmUser
    nullable_fields = ("description", "default_wckey", "default_qos", "admin_level")

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm User"),
                "cluster",
                "default_account",
                "default_wckey",
                "default_qos",
                "admin_level",
            ),
        ]
