# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import PrimaryModelForm, PrimaryModelImportForm, TenancyForm, TenancyImportForm
from coldfront.forms.fields import CSVModelChoiceField, JSONField
from coldfront.slurm.models import SlurmAccount, SlurmAssociation, SlurmCluster, SlurmPartition, SlurmQOS, SlurmUser
from coldfront.users.models.users import Group


class SlurmQOSForm(PrimaryModelForm):
    class Meta:
        model = SlurmQOS
        fields = [
            "name",
            "description",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm QOS"),
                "name",
                "description",
            ),
        ]


class SlurmQOSImportForm(PrimaryModelImportForm):
    class Meta:
        model = SlurmQOS
        fields = [
            "name",
            "description",
            "tags",
        ]


class SlurmClusterForm(TenancyForm, PrimaryModelForm):
    schema = JSONField(
        label=_("Schema"),
        required=False,
        help_text=_("Enter a valid JSON schema to define supported allocation attributes."),
    )

    features = JSONField(
        label=_("Features"),
        required=False,
        help_text=_("Enter valid JSON."),
    )

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

    class Meta:
        model = SlurmCluster
        fields = [
            "name",
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
            Fieldset(
                _("Slurm Accounting"),
                "default_qos",
                "qos_list",
                "fairshare",
                "features",
                "classification",
            ),
        ]


class SlurmClusterImportForm(TenancyImportForm, PrimaryModelImportForm):
    default_qos = CSVModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Default QOS"),
    )

    class Meta:
        model = SlurmCluster
        fields = [
            "name",
            "tenant",
            "description",
            "locked",
            "schema",
            "default_qos",
            "fairshare",
            "features",
            "classification",
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

    max_tres_per_job = JSONField(
        label=_("Max TRES per Job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )

    max_tres_per_node = JSONField(
        label=_("Max TRES per node"),
        required=False,
        help_text=_("Enter valid JSON."),
    )

    max_tres_mins_per_job = JSONField(
        label=_("Max TRES minutes per job"),
        required=False,
        help_text=_("Enter valid JSON."),
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

    class Meta:
        model = SlurmPartition
        fields = [
            "cluster",
            "name",
            "description",
            "locked",
            "schema",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


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
            "max_jobs",
            "max_submit_jobs",
            "max_tres_per_job",
            "max_tres_per_node",
            "max_tres_mins_per_job",
            "max_wall_duration_per_job",
            "fairshare",
            "tags",
        ]


class SlurmAccountForm(PrimaryModelForm):
    cluster = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        label=_("Cluster"),
    )

    qos_list = forms.ModelMultipleChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("QOS List"),
    )

    class Meta:
        model = SlurmAccount
        fields = [
            "cluster",
            "name",
            "description",
            "fairshare",
            "qos_list",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Account"),
                "cluster",
                "name",
                "description",
                "fairshare",
                "qos_list",
            ),
        ]


class SlurmAccountImportForm(PrimaryModelImportForm):
    cluster = CSVModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        to_field_name="name",
        label=_("Cluster"),
    )

    class Meta:
        model = SlurmAccount
        fields = [
            "cluster",
            "name",
            "description",
            "fairshare",
            "tags",
        ]


class SlurmAssociationForm(PrimaryModelForm):
    allocation = forms.ModelChoiceField(
        queryset=SlurmAssociation.objects.all(),  # placeholder, will override __init__
        label=_("Allocation"),
    )

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

    max_tres_per_job = JSONField(
        label=_("Max TRES per Job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )

    max_tres_mins_per_job = JSONField(
        label=_("Max TRES minutes per job"),
        required=False,
        help_text=_("Enter valid JSON."),
    )

    class Meta:
        model = SlurmAssociation
        fields = [
            "allocation",
            "slurm_account",
            "parent",
            "default_qos",
            "fairshare",
            "max_jobs",
            "max_submit_jobs",
            "max_tres_per_job",
            "max_tres_mins_per_job",
            "max_wall_duration_per_job",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm Association"),
                "allocation",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from coldfront.ras.models import Allocation

        self.fields["allocation"] = forms.ModelChoiceField(
            queryset=Allocation.objects.all(),
            label=_("Allocation"),
        )


class SlurmAssociationImportForm(PrimaryModelImportForm):
    allocation = CSVModelChoiceField(
        queryset=SlurmAssociation.objects.all(),  # placeholder, will override __init__
        to_field_name="slug",
        label=_("Allocation"),
    )

    slurm_account = CSVModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Slurm Account"),
    )

    parent = CSVModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Parent Account"),
    )

    default_qos = CSVModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Default QOS"),
    )

    class Meta:
        model = SlurmAssociation
        fields = [
            "allocation",
            "slurm_account",
            "parent",
            "default_qos",
            "fairshare",
            "max_jobs",
            "max_submit_jobs",
            "max_tres_per_job",
            "max_tres_mins_per_job",
            "max_wall_duration_per_job",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from coldfront.ras.models import Allocation

        self.fields["allocation"] = CSVModelChoiceField(
            queryset=Allocation.objects.all(),
            to_field_name="slug",
            label=_("Allocation"),
        )


class SlurmUserForm(PrimaryModelForm):
    user = forms.ModelChoiceField(
        queryset=SlurmUser.objects.all(),  # placeholder, will override __init__
        label=_("User"),
    )

    cluster = forms.ModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        label=_("Cluster"),
    )

    default_account = forms.ModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        label=_("Default Account"),
    )

    default_qos = forms.ModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        required=False,
        label=_("Default QOS"),
    )

    class Meta:
        model = SlurmUser
        fields = [
            "user",
            "cluster",
            "default_account",
            "default_wckey",
            "default_qos",
            "admin_level",
            "tags",
        ]

    @property
    def fieldsets(self):
        return [
            Fieldset(
                _("Slurm User"),
                "user",
                "cluster",
                "default_account",
                "default_wckey",
                "default_qos",
                "admin_level",
            ),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from coldfront.users.models import User

        self.fields["user"] = forms.ModelChoiceField(
            queryset=User.objects.all(),
            label=_("User"),
        )


class SlurmUserImportForm(PrimaryModelImportForm):
    user = CSVModelChoiceField(
        queryset=SlurmUser.objects.none(),  # placeholder, will override __init__
        to_field_name="username",
        label=_("User"),
    )

    cluster = CSVModelChoiceField(
        queryset=SlurmCluster.objects.all(),
        to_field_name="name",
        label=_("Cluster"),
    )

    default_account = CSVModelChoiceField(
        queryset=SlurmAccount.objects.all(),
        to_field_name="name",
        label=_("Default Account"),
    )

    default_qos = CSVModelChoiceField(
        queryset=SlurmQOS.objects.all(),
        to_field_name="name",
        required=False,
        label=_("Default QOS"),
    )

    class Meta:
        model = SlurmUser
        fields = [
            "user",
            "cluster",
            "default_account",
            "default_wckey",
            "default_qos",
            "admin_level",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from coldfront.users.models import User

        self.fields["user"] = CSVModelChoiceField(
            queryset=User.objects.all(),
            to_field_name="username",
            label=_("User"),
        )
