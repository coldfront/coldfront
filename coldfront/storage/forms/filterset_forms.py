# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import gettext_lazy as _

from coldfront.forms import PrimaryModelFilterSetForm
from coldfront.forms.fields import TagFilterField
from coldfront.storage.models import StorageCluster, StorageQuota, StorageResource, StorageSnapshotPolicy


class StorageResourceFilterSetForm(PrimaryModelFilterSetForm):
    model = StorageResource
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Storage Resource"),
            "tag",
        ),
    )


class StorageClusterFilterSetForm(PrimaryModelFilterSetForm):
    model = StorageCluster
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Storage Cluster"),
            "tag",
        ),
    )


class StorageQuotaFilterSetForm(PrimaryModelFilterSetForm):
    model = StorageQuota
    storage_id = forms.ModelChoiceField(
        queryset=StorageResource.objects.all(),
        required=False,
        label=_("Storage Resource"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Storage Quota"),
            "storage_id",
            "tag",
        ),
    )


class StorageSnapshotPolicyFilterSetForm(PrimaryModelFilterSetForm):
    model = StorageSnapshotPolicy
    cluster_id = forms.ModelChoiceField(
        queryset=StorageCluster.objects.all(),
        required=False,
        label=_("Cluster"),
    )
    tag = TagFilterField(model)

    fieldsets = (
        Fieldset(
            _("Snapshot Policy"),
            "cluster_id",
            "tag",
        ),
    )
