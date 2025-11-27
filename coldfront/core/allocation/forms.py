# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from enum import Enum

from django import forms
from django.db.models.functions import Lower
from django.forms import BaseModelFormSet, ValidationError
from django.shortcuts import get_object_or_404

from coldfront.config.core import ALLOCATION_EULA_ENABLE
from coldfront.core.allocation.models import (
    Allocation,
    AllocationAccount,
    AllocationAttribute,
    AllocationAttributeChangeRequest,
    AllocationAttributeType,
    AllocationChangeRequest,
    AllocationStatusChoice,
    AllocationUser,
    AllocationUserNote,
    AllocationUserStatusChoice,
)
from coldfront.core.allocation.utils import get_user_resources
from coldfront.core.project.models import Project
from coldfront.core.resource.models import Resource, ResourceType
from coldfront.core.utils.common import import_from_settings

ALLOCATION_ACCOUNT_ENABLED = import_from_settings("ALLOCATION_ACCOUNT_ENABLED", False)
ALLOCATION_CHANGE_REQUEST_EXTENSION_DAYS = import_from_settings("ALLOCATION_CHANGE_REQUEST_EXTENSION_DAYS", [])
ALLOCATION_ACCOUNT_MAPPING = import_from_settings("ALLOCATION_ACCOUNT_MAPPING", {})
ALLOCATION_ENABLE_CHANGE_REQUESTS_BY_DEFAULT = import_from_settings(
    "ALLOCATION_ENABLE_CHANGE_REQUESTS_BY_DEFAULT", True
)

INVOICE_ENABLED = import_from_settings("INVOICE_ENABLED", False)
if INVOICE_ENABLED:
    INVOICE_DEFAULT_STATUS = import_from_settings("INVOICE_DEFAULT_STATUS", "Pending Payment")


class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = [
            "resource",
            "justification",
            "quantity",
            "users",
            "project",
            "is_changeable",
        ]
        help_texts = {
            "justification": "<br/>Justification for requesting this allocation.",
            "users": "<br/>Select users in your project to add to this allocation.",
        }
        widgets = {
            "status": forms.HiddenInput(),
            "project": forms.HiddenInput(),
            "is_changeable": forms.HiddenInput(),
        }

    resource = forms.ModelChoiceField(queryset=None, empty_label=None)
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
    allocation_account = forms.ChoiceField(required=False)

    def __init__(self, request_user, project_pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_obj = get_object_or_404(Project, pk=project_pk)

        # Set initial values
        self.fields["quantity"].initial = 1
        self.fields["is_changeable"].initial = ALLOCATION_ENABLE_CHANGE_REQUESTS_BY_DEFAULT
        self.fields["project"].initial = project_obj

        self.fields["resource"].queryset = get_user_resources(request_user).order_by(Lower("name"))

        # Set user choices
        user_query_set = (
            project_obj.projectuser_set.select_related("user")
            .filter(status__name__in=["Active"])
            .order_by("user__username")
            .exclude(user=project_obj.pi)
        )
        if user_query_set:
            self.fields["users"].choices = (
                (user.user.username, "%s %s (%s)" % (user.user.first_name, user.user.last_name, user.user.username))
                for user in user_query_set
            )
        else:
            self.fields["users"].widget = forms.HiddenInput()

        # Set allocation_account choices
        if ALLOCATION_ACCOUNT_ENABLED:
            allocation_accounts = AllocationAccount.objects.filter(user=request_user)
            if allocation_accounts:
                self.fields["allocation_account"].choices = (
                    (account.name, account.name) for account in allocation_accounts
                )
        else:
            self.fields["allocation_account"].widget = forms.HiddenInput()

    def clean(self):
        form_data = super().clean()
        project_obj = form_data.get("project")
        resource_obj = form_data.get("resource")
        allocation_account = form_data.get("allocation_account", None)

        # Ensure user has account name if ALLOCATION_ACCOUNT_ENABLED
        if (
            ALLOCATION_ACCOUNT_ENABLED
            and resource_obj.name in ALLOCATION_ACCOUNT_MAPPING
            and AllocationAttributeType.objects.filter(name=ALLOCATION_ACCOUNT_MAPPING[resource_obj.name]).exists()
            and not allocation_account
        ):
            raise ValidationError(
                'You need to create an account name. Create it by clicking the link under the "Allocation account" field.',
                code="user_has_no_account_name",
            )

        # Ensure this allocaiton wouldn't exceed the limit
        allocation_limit = resource_obj.get_attribute("allocation_limit", typed=True)
        if allocation_limit:
            allocation_count = project_obj.allocation_set.filter(
                resources=resource_obj,
                status__name__in=["Active", "New", "Renewal Requested", "Paid", "Payment Pending", "Payment Requested"],
            ).count()
            if allocation_count >= allocation_limit:
                raise ValidationError(
                    "Your project is at the allocation limit allowed for this resource.",
                    code="reached_allocation_limit",
                )

        # Set allocation status
        if INVOICE_ENABLED and resource_obj.requires_payment:
            allocation_status_name = INVOICE_DEFAULT_STATUS
        else:
            allocation_status_name = "New"
        form_data["status"] = AllocationStatusChoice.objects.get(name=allocation_status_name)
        self.instance.status = form_data["status"]

        return form_data


class AllocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = [
            "status",
            "start_date",
            "end_date",
            "description",
            "is_locked",
            "is_changeable",
        ]

    status = forms.ModelChoiceField(
        queryset=AllocationStatusChoice.objects.all().order_by(Lower("name")), empty_label=None
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={"class": "datepicker"}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={"class": "datepicker"}), required=False)

    def __init__(self, request_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not request_user.is_superuser:
            self.fields["is_locked"].disabled = True
            self.fields["is_changeable"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be less than start date")


class AllocationInvoiceUpdateForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=AllocationStatusChoice.objects.filter(
            name__in=["Payment Pending", "Payment Requested", "Payment Declined", "Paid"]
        ).order_by(Lower("name")),
        empty_label=None,
    )


class AllocationUserForm(forms.ModelForm):
    class Meta:
        model = AllocationUser
        fields = ["allocation", "user", "status"]
        widgets = {
            "allocation": forms.HiddenInput(),
            "user": forms.HiddenInput(),
            "status": forms.HiddenInput(),
        }

    selected = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].disabled = True


class BaseAllocationUserFormSet(BaseModelFormSet):
    template_name = "allocation/forms/formsets/allocation_user_formset.html"

    class Action(Enum):
        ADD = 1
        REMOVE = 2

    def __init__(self, action: Action, *args, **kwargs):
        self.action = action
        super().__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if not form.cleaned_data.get("selected"):
                continue

            user = form.cleaned_data.get("user")
            allocation = form.cleaned_data.get("allocation")

            if self.action == self.Action.ADD:
                user_is_pending_eula = ALLOCATION_EULA_ENABLE and not user.userprofile.is_pi and allocation.get_eula()
                if user_is_pending_eula:
                    allocation_user_status = AllocationUserStatusChoice.objects.get(name="PendingEULA")
                    form.cleaned_data["status"] = allocation_user_status
                    form.instance.status = form.cleaned_data["status"]
            elif self.action == self.Action.REMOVE:
                if allocation.project.pi == user:
                    raise ValidationError("Cannot remove the project PI from an allocation.")


class AllocationSearchForm(forms.Form):
    project = forms.CharField(label="Project Title", max_length=100, required=False)
    username = forms.CharField(label="Username", max_length=100, required=False)
    resource_type = forms.ModelChoiceField(
        label="Resource Type", queryset=ResourceType.objects.all().order_by(Lower("name")), required=False
    )
    resource_name = forms.ModelMultipleChoiceField(
        label="Resource Name",
        queryset=Resource.objects.filter(is_allocatable=True).order_by(Lower("name")),
        required=False,
    )
    allocation_attribute_name = forms.ModelChoiceField(
        label="Allocation Attribute Name",
        queryset=AllocationAttributeType.objects.all().order_by(Lower("name")),
        required=False,
    )
    allocation_attribute_value = forms.CharField(label="Allocation Attribute Value", max_length=100, required=False)
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(attrs={"class": "datepicker"}), required=False)
    active_from_now_until_date = forms.DateField(
        label="Active from Now Until Date", widget=forms.DateInput(attrs={"class": "datepicker"}), required=False
    )
    status = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=AllocationStatusChoice.objects.all().order_by(Lower("name")),
        required=False,
    )
    show_all_allocations = forms.BooleanField(initial=False, required=False)


class AllocationReviewUserForm(forms.ModelForm):
    class Meta:
        model = AllocationUser
        fields = ["allocation", "user", "status"]
        widgets = {"allocation": forms.HiddenInput()}

    ALLOCATION_REVIEW_USER_CHOICES = (
        ("keep_in_allocation_and_project", "Keep in allocation and project"),
        ("keep_in_project_only", "Remove from this allocation only"),
        ("remove_from_project", "Remove from project"),
    )

    user_status = forms.ChoiceField(choices=ALLOCATION_REVIEW_USER_CHOICES)

    def __init__(self, disabled_fields=["allocation"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in disabled_fields:
            self.fields[field].disabled = True

    def save(self, commit=True):
        # Not calling super().save() here - We need to do more than update
        # the AllocationUser, so it will be less confusing to change the
        # status of the AllocationUser/ProjectUser here.
        cleaned_data = self.cleaned_data
        user_status = cleaned_data.get("user_status")
        allocation = cleaned_data.get("allocation")
        user = cleaned_data.get("user")
        if user_status == "keep_in_project_only":
            allocation.remove_user(user, signal_sender=self.__class__)
        elif user_status == "remove_from_project":
            allocation.project.remove_user(user, signal_sender=self.__class__)


class AllocationInvoiceNoteForm(forms.ModelForm):
    class Meta:
        model = AllocationUserNote
        fields = ["allocation", "author", "is_private", "note"]
        widgets = {
            "allocation": forms.HiddenInput(),
            "author": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["allocation"].disabled = True
        self.fields["author"].disabled = True


class AllocationAccountForm(forms.ModelForm):
    class Meta:
        model = AllocationAccount
        fields = ["name"]


class AllocationChangeRequestForm(forms.ModelForm):
    class Meta:
        model = AllocationChangeRequest
        fields = [
            "allocation",
            "status",
            "end_date_extension",
            "justification",
            "notes",
        ]
        widgets = {
            "allocation": forms.HiddenInput(),
            "status": forms.HiddenInput(),
            "notes": forms.Textarea(),
        }
        labels = {"justification": "Justification for Changes"}
        help_texts = {"justification": "Justification for requesting this allocation change request."}

    EXTENSION_CHOICES = [(0, "No Extension")]
    for choice in ALLOCATION_CHANGE_REQUEST_EXTENSION_DAYS:
        EXTENSION_CHOICES.append((choice, "{} days".format(choice)))

    end_date_extension = forms.TypedChoiceField(
        label="Request End Date Extension",
        choices=EXTENSION_CHOICES,
        coerce=int,
        required=False,
        empty_value=0,
    )

    def __init__(self, disabled_fields=["allocation"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in disabled_fields:
            self.fields[field].disabled = True

    def has_changed(self):
        # We con't care if "justification" nor "notes" has been changed.
        changed_data = set(self.changed_data)
        changed_data -= {"justification", "notes"}
        return bool(changed_data)


class AllocationAttributeChangeRequestForm(forms.ModelForm):
    class Meta:
        model = AllocationAttributeChangeRequest
        fields = ["allocation_change_request", "allocation_attribute", "new_value"]
        widgets = {"allocation_attribute": forms.HiddenInput()}

    allocation_change_request = forms.ModelChoiceField(
        queryset=AllocationChangeRequest.objects.all(),
        disabled=True,
        widget=forms.HiddenInput(),
    )

    def clean(self):
        form_data = super().clean()
        allocation_attribute = form_data.get("allocation_attribute")
        new_value = form_data.get("new_value")
        if allocation_attribute.value == new_value:
            raise ValidationError(
                "New value (%(value)s) cannot be the same as current value for %(attribute)s.",
                code="no_change_requested",
                params={"value": new_value, "attribute": allocation_attribute},
            )
        if form_data.get("new_value") != "":
            allocation_attribute.value = form_data.get("new_value")
            allocation_attribute.clean()
        return form_data


class AllocationAttributeForm(forms.ModelForm):
    class Meta:
        model = AllocationAttribute
        fields = ["allocation_attribute_type", "allocation", "value"]
        widgets = {"allocation": forms.HiddenInput()}

    def __init__(self, disabled_fields=["allocation"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["allocation_attribute_type"].queryset = self.fields["allocation_attribute_type"].queryset.order_by(
            Lower("name")
        )
        for field in disabled_fields:
            self.fields[field].disabled = True
