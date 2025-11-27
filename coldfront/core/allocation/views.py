# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import datetime
import logging
from datetime import date

from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import pluralize
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import (
    CreateView,
    FormView,
    UpdateView,
)

from coldfront.config.core import ALLOCATION_EULA_ENABLE
from coldfront.core.allocation.forms import (
    AllocationAccountForm,
    AllocationAttributeChangeRequestForm,
    AllocationAttributeForm,
    AllocationChangeRequestForm,
    AllocationForm,
    AllocationInvoiceNoteForm,
    AllocationInvoiceUpdateForm,
    AllocationReviewUserForm,
    AllocationSearchForm,
    AllocationUpdateForm,
    AllocationUserForm,
    BaseAllocationUserFormSet,
)
from coldfront.core.allocation.models import (
    Allocation,
    AllocationAccount,
    AllocationAttribute,
    AllocationAttributeChangeRequest,
    AllocationAttributeType,
    AllocationChangeRequest,
    AllocationChangeStatusChoice,
    AllocationPermission,
    AllocationStatusChoice,
    AllocationUser,
    AllocationUserNote,
    AllocationUserStatusChoice,
)
from coldfront.core.allocation.signals import (
    allocation_activate,
    allocation_activate_user,
    allocation_attribute_changed,
    allocation_change_approved,
    allocation_change_created,
    allocation_disable,
    allocation_new,
    allocation_remove_user,
)
from coldfront.core.allocation.utils import generate_guauge_data_from_usage, get_user_resources
from coldfront.core.project.models import Project, ProjectPermission
from coldfront.core.resource.models import Resource
from coldfront.core.utils.common import get_domain_url, import_from_settings
from coldfront.core.utils.mail import (
    send_allocation_admin_email,
    send_allocation_customer_email,
    send_allocation_eula_customer_email,
)
from coldfront.core.utils.mixins.views import AllocationInContextView
from coldfront.core.utils.views import FormErrorsInMessagesMixin, ModelFormSetView

ALLOCATION_ENABLE_ALLOCATION_RENEWAL = import_from_settings("ALLOCATION_ENABLE_ALLOCATION_RENEWAL", True)
ALLOCATION_DEFAULT_ALLOCATION_LENGTH = import_from_settings("ALLOCATION_DEFAULT_ALLOCATION_LENGTH", 365)
ALLOCATION_ENABLE_CHANGE_REQUESTS_BY_DEFAULT = import_from_settings(
    "ALLOCATION_ENABLE_CHANGE_REQUESTS_BY_DEFAULT", True
)

PROJECT_ENABLE_PROJECT_REVIEW = import_from_settings("PROJECT_ENABLE_PROJECT_REVIEW", False)
INVOICE_ENABLED = import_from_settings("INVOICE_ENABLED", False)
if INVOICE_ENABLED:
    INVOICE_DEFAULT_STATUS = import_from_settings("INVOICE_DEFAULT_STATUS", "Pending Payment")

ALLOCATION_ACCOUNT_ENABLED = import_from_settings("ALLOCATION_ACCOUNT_ENABLED", False)
ALLOCATION_ACCOUNT_MAPPING = import_from_settings("ALLOCATION_ACCOUNT_MAPPING", {})

EMAIL_ALLOCATION_EULA_IGNORE_OPT_OUT = import_from_settings("EMAIL_ALLOCATION_EULA_IGNORE_OPT_OUT", False)
EMAIL_ALLOCATION_EULA_CONFIRMATIONS = import_from_settings("EMAIL_ALLOCATION_EULA_CONFIRMATIONS", False)
EMAIL_ALLOCATION_EULA_CONFIRMATIONS_CC_MANAGERS = import_from_settings(
    "EMAIL_ALLOCATION_EULA_CONFIRMATIONS_CC_MANAGERS", False
)
EMAIL_ALLOCATION_EULA_INCLUDE_ACCEPTED_EULA = import_from_settings("EMAIL_ALLOCATION_EULA_INCLUDE_ACCEPTED_EULA", False)

logger = logging.getLogger(__name__)


class AllocationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView, UpdateView):
    model = Allocation
    form_class = AllocationUpdateForm
    template_name = "allocation/allocation_detail.html"
    context_object_name = "allocation"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)

        if self.request.user.has_perm("allocation.can_view_all_allocations"):
            return True

        return allocation_obj.has_perm(self.request.user, AllocationPermission.USER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)
        allocation_users = allocation_obj.allocationuser_set.exclude(
            status__name__in=[
                "Removed",
            ]
        ).order_by("user__username")

        if ALLOCATION_EULA_ENABLE:
            user_in_allocation = allocation_users.filter(user=self.request.user).exists()
            context["user_in_allocation"] = user_in_allocation

            if user_in_allocation:
                allocation_user_status = get_object_or_404(
                    AllocationUser, allocation=allocation_obj, user=self.request.user
                ).status
                if allocation_obj.status.name == "Active" and allocation_user_status.name == "PendingEula":
                    messages.info(self.request, "This allocation is active, but you must agree to the EULA to use it!")

            context["eulas"] = allocation_obj.get_eula()
            context["res"] = allocation_obj.get_parent_resource.pk
            context["res_obj"] = allocation_obj.get_parent_resource

        # set visible usage attributes
        alloc_attr_set = allocation_obj.get_attribute_set(self.request.user)
        attributes_with_usage = [a for a in alloc_attr_set if hasattr(a, "allocationattributeusage")]
        attributes = alloc_attr_set

        allocation_changes = allocation_obj.allocationchangerequest_set.all().order_by("-pk")

        guage_data = []
        invalid_attributes = []
        for attribute in attributes_with_usage:
            try:
                guage_data.append(
                    generate_guauge_data_from_usage(
                        attribute.allocation_attribute_type.name,
                        float(attribute.value),
                        float(attribute.allocationattributeusage.value),
                    )
                )
            except ValueError:
                logger.error(
                    "Allocation attribute '%s' is not an int but has a usage", attribute.allocation_attribute_type.name
                )
                invalid_attributes.append(attribute)

        for a in invalid_attributes:
            attributes_with_usage.remove(a)

        context["allocation_users"] = allocation_users
        context["guage_data"] = guage_data
        context["attributes_with_usage"] = attributes_with_usage
        context["attributes"] = attributes
        context["allocation_changes"] = allocation_changes

        # Can the user update the project?
        context["is_allowed_to_update_project"] = allocation_obj.project.has_perm(
            self.request.user, ProjectPermission.UPDATE
        )

        noteset = allocation_obj.allocationusernote_set
        notes = noteset.all() if self.request.user.is_superuser else noteset.filter(is_private=False)

        context["notes"] = notes
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request_user": self.request.user})
        return kwargs

    def get_success_url(self):
        if self.request.method == "POST":
            action = self.request.POST.get("action")
            if action == "auto-approve":
                return reverse("allocation-request-list")
        return reverse("allocation-detail", kwargs={"pk": self.kwargs.get("pk")})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.is_superuser:
            messages.success(request, "You do not have permission to update the allocation")
            return redirect(self.object)

        action = request.POST.get("action")
        if action not in ["update", "approve", "auto-approve", "deny"]:
            return HttpResponseBadRequest("Invalid request")

        # form pre-processing
        form_kwargs = self.get_form_kwargs()
        dirty_form_data = form_kwargs["data"].copy()

        if action in ["approve", "auto-approve"]:
            dirty_form_data["status"] = AllocationStatusChoice.objects.get(name="Active").pk
        elif action == "deny":
            dirty_form_data["status"] = AllocationStatusChoice.objects.get(name="Denied").pk

        old_status = self.object.status.name
        new_status = AllocationStatusChoice.objects.get(pk=dirty_form_data.get("status")).name
        status_changed = old_status != new_status
        allocation_signal = None
        allocation_user_signal = None
        allocation_user_qs = None
        email_kwargs = None

        if not status_changed:
            return super().post(request, *args, **kwargs)

        if new_status == "Active":
            now = datetime.datetime.now()
            if not self.object.start_date:
                dirty_form_data["start_date"] = now
            if action in ["approve", "auto-approve"] or not dirty_form_data["end_date"]:
                dirty_form_data["end_date"] = now + relativedelta(days=ALLOCATION_DEFAULT_ALLOCATION_LENGTH)

            allocation_signal = allocation_activate
            allocation_user_qs = self.object.allocationuser_set.exclude(
                status__name__in=["Removed", "Error", "DeclinedEULA", "PendingEULA"]
            )
            allocation_user_signal = allocation_activate_user
            email_kwargs = {
                "subject": "Allocation Activated",
                "template_name": "email/allocation_activated.txt",
            }

            # set message
            if action != "auto-approve":
                messages.success(request, "Allocation Activated!")
            elif action == "auto-approve":
                messages.success(
                    request,
                    "Allocation to {} has been ACTIVATED for {} {} ({})".format(
                        self.object.get_parent_resource,
                        self.object.project.pi.first_name,
                        self.object.project.pi.last_name,
                        self.object.project.pi.username,
                    ),
                )
        elif new_status in ["Denied", "New", "Revoked"]:
            dirty_form_data["start_date"] = None
            dirty_form_data["end_date"] = None

            if new_status in ["Denied", "Revoked"]:
                allocation_signal = allocation_disable
                allocation_user_qs = self.object.allocationuser_set.exclude(status__name__in=["Removed", "Error"])
                allocation_user_signal = allocation_remove_user

                if new_status == "Denied":
                    email_kwargs = {
                        "subject": "Allocation Denied",
                        "template_name": "email/allocation_denied.txt",
                    }
                    messages.success(request, "Allocation Denied!")
                elif new_status == "Revoked":
                    email_kwargs = {
                        "subject": "Allocation Revoked",
                        "template_name": "email/allocation_revoked.txt",
                    }
                    messages.success(request, "Allocation Revoked!")
            else:
                messages.success(request, "Allocation updated!")

        form_kwargs["data"] = dirty_form_data
        form_class = self.get_form_class()
        form = form_class(**form_kwargs)
        if form.is_valid():
            # save form and perform post-save actions
            redirect = self.form_valid(form)
            if allocation_signal:
                allocation_signal.send(sender=self.__class__, allocation_pk=self.object.pk)
            if allocation_user_signal and allocation_user_qs:
                for allocation_user in allocation_user_qs:
                    allocation_user_signal.send(sender=self.__class__, allocation_user_pk=allocation_user.pk)
            if email_kwargs:
                send_allocation_customer_email(
                    allocation_obj=self.object, domain_url=get_domain_url(self.request), **email_kwargs
                )
        else:
            redirect = self.form_invalid(form)

        return redirect


class AllocationEULAView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = Allocation
    template_name = "allocation/allocation_review_eula.html"
    context_object_name = "allocation-eula"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)

        if self.request.user.has_perm("allocation.can_view_all_allocations"):
            return True

        return allocation_obj.has_perm(self.request.user, AllocationPermission.USER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)
        allocation_users = allocation_obj.allocationuser_set.exclude(
            status__name__in=[
                "Removed",
            ]
        ).order_by("user__username")
        user_in_allocation = allocation_users.filter(user=self.request.user).exists()

        context["allocation"] = allocation_obj.pk
        context["eulas"] = allocation_obj.get_eula()
        context["res"] = allocation_obj.get_parent_resource.pk
        context["res_obj"] = allocation_obj.get_parent_resource

        if user_in_allocation and ALLOCATION_EULA_ENABLE:
            allocation_user_status = get_object_or_404(
                AllocationUser, allocation=allocation_obj, user=self.request.user
            ).status
            context["allocation_user_status"] = allocation_user_status.name
            context["last_updated"] = get_object_or_404(
                AllocationUser, allocation=allocation_obj, user=self.request.user
            ).modified

        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        get_object_or_404(Allocation, pk=pk)
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)
        allocation_users = allocation_obj.allocationuser_set.exclude(
            status__name__in=["Removed", "DeclinedEULA"]
        ).order_by("user__username")
        user_in_allocation = allocation_users.filter(user=self.request.user).exists()
        if user_in_allocation:
            allocation_user_obj = get_object_or_404(AllocationUser, allocation=allocation_obj, user=self.request.user)
            action = request.POST.get("action")
            if action not in ["accepted_eula", "declined_eula"]:
                return HttpResponseBadRequest("Invalid request")
            if "accepted_eula" in action:
                allocation_user_obj.status = AllocationUserStatusChoice.objects.get(name="Active")
                messages.success(self.request, "EULA Accepted!")
                if EMAIL_ALLOCATION_EULA_CONFIRMATIONS:
                    project_user = allocation_user_obj.allocation.project.projectuser_set.get(
                        user=allocation_user_obj.user
                    )
                    if EMAIL_ALLOCATION_EULA_IGNORE_OPT_OUT or project_user.enable_notifications:
                        send_allocation_eula_customer_email(
                            allocation_user_obj,
                            "EULA accepted",
                            "email/allocation_eula_accepted.txt",
                            cc_managers=EMAIL_ALLOCATION_EULA_CONFIRMATIONS_CC_MANAGERS,
                            include_eula=EMAIL_ALLOCATION_EULA_INCLUDE_ACCEPTED_EULA,
                        )
                allocation_obj.activate_user(allocation_user_obj, signal_sender=self.__class__)
            elif action == "declined_eula":
                allocation_user_obj.status = AllocationUserStatusChoice.objects.get(name="DeclinedEULA")
                messages.warning(
                    self.request,
                    "You did not agree to the EULA and were removed from the allocation. To access this allocation, your PI will have to re-add you.",
                )
                if EMAIL_ALLOCATION_EULA_CONFIRMATIONS:
                    project_user = allocation_user_obj.allocation.project.projectuser_set.get(
                        user=allocation_user_obj.user
                    )
                    if EMAIL_ALLOCATION_EULA_IGNORE_OPT_OUT or project_user.enable_notifications:
                        send_allocation_eula_customer_email(
                            allocation_user_obj,
                            "EULA declined",
                            "email/allocation_eula_declined.txt",
                            cc_managers=EMAIL_ALLOCATION_EULA_CONFIRMATIONS_CC_MANAGERS,
                        )
            allocation_user_obj.save()

        return HttpResponseRedirect(reverse("allocation-review-eula", kwargs={"pk": pk}))


class AllocationListView(LoginRequiredMixin, ListView):
    model = Allocation
    template_name = "allocation/allocation_list.html"
    context_object_name = "allocation_list"
    paginate_by = 25

    def get_queryset(self):
        order_by = self.request.GET.get("order_by")
        if order_by:
            direction = self.request.GET.get("direction")
            dir_dict = {"asc": "", "des": "-"}
            order_by = dir_dict[direction] + order_by
        else:
            order_by = "id"

        allocation_search_form = AllocationSearchForm(self.request.GET)
        allocations = Allocation.objects.prefetch_related("project", "project__pi", "status").order_by(order_by)

        if not allocation_search_form.is_valid():
            allocations = allocations.filter(
                Q(allocationuser__user=self.request.user)
                & Q(allocationuser__status__name__in=["PendingEULA", "Active"])
            ).distinct()
            return allocations

        data = allocation_search_form.cleaned_data

        if data.get("show_all_allocations") and (
            self.request.user.is_superuser or self.request.user.has_perm("allocation.can_view_all_allocations")
        ):
            allocations = allocations.all()
        else:
            allocations = allocations.filter(
                Q(project__status__name__in=["New", "Active"])
                & Q(project__projectuser__status__name__in=["Active"])
                & Q(project__projectuser__user=self.request.user)
                & (
                    Q(project__projectuser__role__name="Manager")
                    | Q(allocationuser__user=self.request.user)
                    & Q(allocationuser__status__name__in=["Active", "PendingEULA"])
                )
            )

        # Project Title
        if data.get("project"):
            allocations = allocations.filter(project__title__icontains=data.get("project"))

        # username
        if data.get("username"):
            allocations = allocations.filter(
                Q(project__pi__username__icontains=data.get("username"))
                | Q(allocationuser__user__username__icontains=data.get("username"))
                & Q(allocationuser__status__name__in=["PendingEULA", "Active"])
            )

        # Resource Type
        if data.get("resource_type"):
            allocations = allocations.filter(resources__resource_type=data.get("resource_type"))

        # Resource Name
        if data.get("resource_name"):
            allocations = allocations.filter(resources__in=data.get("resource_name"))

        # Allocation Attribute Name
        if data.get("allocation_attribute_name") and data.get("allocation_attribute_value"):
            allocations = allocations.filter(
                Q(allocationattribute__allocation_attribute_type=data.get("allocation_attribute_name"))
                & Q(allocationattribute__value=data.get("allocation_attribute_value"))
            )

        # End Date
        if data.get("end_date"):
            allocations = allocations.filter(end_date__lt=data.get("end_date"), status__name="Active").order_by(
                "end_date"
            )

        # Active from now until date
        if data.get("active_from_now_until_date"):
            allocations = allocations.filter(end_date__gte=date.today())
            allocations = allocations.filter(
                end_date__lt=data.get("active_from_now_until_date"), status__name="Active"
            ).order_by("end_date")

        # Status
        if data.get("status"):
            allocations = allocations.filter(status__in=data.get("status"))

        return allocations.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allocations_count = self.get_queryset().count()
        context["allocations_count"] = allocations_count

        allocation_search_form = AllocationSearchForm(self.request.GET)

        if allocation_search_form.is_valid():
            data = allocation_search_form.cleaned_data
            filter_parameters = ""
            for key, value in data.items():
                if not value:
                    continue
                if isinstance(value, QuerySet):
                    filter_parameters += "".join([f"{key}={ele.pk}&" for ele in value])
                elif hasattr(value, "pk"):
                    filter_parameters += f"{key}={value.pk}&"
                else:
                    filter_parameters += f"{key}={value}&"
            context["allocation_search_form"] = allocation_search_form
        else:
            filter_parameters = None
            context["allocation_search_form"] = AllocationSearchForm()

        filter_parameters_with_order_by = filter_parameters
        order_by = self.request.GET.get("order_by")
        if order_by:
            direction = self.request.GET.get("direction")
            filter_parameters_with_order_by += "order_by=%s&direction=%s&" % (order_by, direction)

        if filter_parameters:
            context["expand_accordion"] = "show"
        context["filter_parameters"] = filter_parameters
        context["filter_parameters_with_order_by"] = filter_parameters_with_order_by

        allocation_list = context.get("allocation_list")
        paginator = Paginator(allocation_list, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            allocation_list = paginator.page(page)
        except PageNotAnInteger:
            allocation_list = paginator.page(1)
        except EmptyPage:
            allocation_list = paginator.page(paginator.num_pages)

        return context


class AllocationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AllocationForm
    template_name = "allocation/allocation_create.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))
        if project_obj.has_perm(self.request.user, ProjectPermission.UPDATE):
            return True

        messages.error(self.request, "You do not have permission to create a new allocation.")
        return False

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))

        if project_obj.needs_review:
            messages.error(
                request, "You cannot request a new allocation because you have to review your project first."
            )
            return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))

        if project_obj.status.name not in [
            "Active",
            "New",
        ]:
            messages.error(request, "You cannot request a new allocation to an archived project.")
            return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))
        context["project"] = project_obj

        user_resources = get_user_resources(self.request.user)
        resources_dict = {
            "quantity_default_value": {},
            "form_description": {},
            "quantity_label": {},
            "eula": {},
        }
        for resource in user_resources:
            for attr_name in resources_dict.keys():
                query = Q(resource_attribute_type__name=attr_name)
                if not resource.resourceattribute_set.filter(query).exists():
                    continue
                value = resource.resourceattribute_set.get(query).value
                if attr_name == "quantity_default_value":
                    resources_dict[attr_name][resource.id] = int(value)
                else:
                    resources_dict[attr_name][resource.id] = value

        context["resources_form_default_quantities"] = resources_dict["quantity_default_value"]
        context["resources_form_descriptions"] = resources_dict["form_description"]
        context["resources_form_label_texts"] = resources_dict["quantity_label"]
        context["resources_with_eula"] = resources_dict["eula"]
        context["resources_with_accounts"] = list(
            Resource.objects.filter(name__in=list(ALLOCATION_ACCOUNT_MAPPING.keys())).values_list("id", flat=True)
        )

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "request_user": self.request.user,
                "project_pk": self.kwargs.get("project_pk"),
            }
        )
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        form_data = form.cleaned_data
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))
        resource_obj = form_data.get("resource")
        allocation_account = form_data.get("allocation_account", None)

        # add users to allocation
        usernames = form_data.get("users")
        usernames.append(project_obj.pi.username)
        usernames = set(usernames)
        allocation_user_active_status = AllocationUserStatusChoice.objects.get(name="Active")
        if ALLOCATION_EULA_ENABLE:
            allocation_user_pending_status = AllocationUserStatusChoice.objects.get(name="PendingEULA")
        alloc_user_kwargs = [
            {
                "user": get_user_model().objects.get(username=username),
                "status": allocation_user_pending_status
                if ALLOCATION_EULA_ENABLE and username != self.request.user.username
                else allocation_user_active_status,
            }
            for username in usernames
        ]
        for kwargs in alloc_user_kwargs:
            self.object.allocationuser_set.create(**kwargs)

        # add resources to allocation
        self.object.resources.add(resource_obj)
        for linked_resource in resource_obj.linked_resources.all():
            self.object.resources.add(linked_resource)

        # add allocation account attribute to allocation
        if ALLOCATION_ACCOUNT_ENABLED and allocation_account and resource_obj.name in ALLOCATION_ACCOUNT_MAPPING:
            allocation_attribute_type_obj = AllocationAttributeType.objects.get(
                name=ALLOCATION_ACCOUNT_MAPPING[resource_obj.name]
            )
            self.object.allocationattribute_set.create(
                allocation_attribute_type=allocation_attribute_type_obj,
                value=allocation_account,
            )

        send_allocation_admin_email(
            self.object,
            "New Allocation Request",
            "email/new_allocation_request.txt",
            domain_url=get_domain_url(self.request),
        )
        allocation_new.send(sender=self.__class__, allocation_pk=self.object.pk)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Allocation requested. It will be available once it is approved.")
        return reverse("project-detail", kwargs={"pk": self.kwargs.get("project_pk")})


class AllocationUsersAddView(LoginRequiredMixin, UserPassesTestMixin, AllocationInContextView, ModelFormSetView):
    formset_model = AllocationUser
    formset_form_class = AllocationUserForm
    template_name = "allocation/allocation_add_users.html"
    formset_prefix = "userform"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        if allocation_obj.has_perm(self.request.user, AllocationPermission.MANAGER):
            return True

        messages.error(self.request, "You do not have permission to add users to the allocation.")
        return False

    def dispatch(self, request, *args, **kwargs):
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))

        message = None
        if allocation_obj.is_locked and not self.request.user.is_superuser:
            message = "You cannot modify this allocation because it is locked! Contact support for details."
        elif allocation_obj.status.name not in [
            "Active",
            "New",
            "Renewal Requested",
            "Payment Pending",
            "Payment Requested",
            "Paid",
        ]:
            message = f"You cannot add users to an allocation with status {allocation_obj.status.name}."
        if message:
            messages.error(request, message)
            return redirect(allocation_obj)
        return super().dispatch(request, *args, **kwargs)

    def get_formset_queryset(self):
        return self.allocation.allocationuser_set.filter(status__name__in=["Removed"])

    def get_formset_initial(self):
        project_user_pks = set(
            self.allocation.project.projectuser_set.filter(status__name="Active").values_list("user__pk", flat=True)
        )
        allocation_user_pks = set(self.allocation.allocationuser_set.values_list("user__pk", flat=True))
        missing_user_pks = project_user_pks - allocation_user_pks
        missing_user_pks.discard(self.allocation.project.pi.pk)
        missing_users = get_user_model().objects.filter(pk__in=missing_user_pks)

        allocation_user_status_name = "PendingEULA" if ALLOCATION_EULA_ENABLE else "Active"
        allocation_user_status = AllocationUserStatusChoice.objects.get(name=allocation_user_status_name)

        users_to_add = [
            {
                "allocation": self.allocation,
                "user": user,
                "status": allocation_user_status,
            }
            for user in missing_users
        ]
        return users_to_add

    def get_formset_factory_kwargs(self):
        kwargs = super().get_formset_factory_kwargs()
        kwargs["formset"] = BaseAllocationUserFormSet
        return kwargs

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        allocation_user_status_name = "PendingEULA" if ALLOCATION_EULA_ENABLE else "Active"
        allocation_user_status = AllocationUserStatusChoice.objects.get(name=allocation_user_status_name)
        kwargs.update(
            {
                "action": BaseAllocationUserFormSet.Action.ADD,
                "form_kwargs": {"initial": {"status": allocation_user_status}},
            }
        )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_resources = get_user_resources(self.request.user)
        resources_with_eula = {}
        for res in user_resources:
            if res in self.allocation.get_resources_as_list:
                for attr_value in res.get_attribute_list(name="eula"):
                    resources_with_eula[res] = attr_value

        context["resources_with_eula"] = resources_with_eula
        string_accumulator = ""
        for res, value in resources_with_eula.items():
            string_accumulator += f"{res}: {value}\n"
        context["compiled_eula"] = str(string_accumulator)

        return context

    def formset_valid(self, formset):
        redirect = super().formset_valid(formset)
        allocation_users = self.objects
        for allocation_user in allocation_users:
            self.allocation.add_user(allocation_user.user, signal_sender=self.__class__)
        users_added_count = len(allocation_users)
        messages.success(self.request, f"Added {users_added_count} user{pluralize(users_added_count)} to allocation.")
        return redirect


class AllocationUsersRemoveView(LoginRequiredMixin, UserPassesTestMixin, AllocationInContextView, ModelFormSetView):
    formset_model = AllocationUser
    formset_form_class = AllocationUserForm
    template_name = "allocation/allocation_remove_users.html"
    formset_prefix = "userform"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        if allocation_obj.has_perm(self.request.user, AllocationPermission.MANAGER):
            return True

        messages.error(self.request, "You do not have permission to remove users from allocation.")
        return False

    def dispatch(self, request, *args, **kwargs):
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))

        message = None
        if allocation_obj.is_locked and not self.request.user.is_superuser:
            message = "You cannot modify this allocation because it is locked! Contact support for details."
        elif allocation_obj.status.name not in [
            "Active",
            "New",
            "Renewal Requested",
        ]:
            message = f"You cannot remove users from a allocation with status {allocation_obj.status.name}."
        if message:
            messages.error(request, message)
            return redirect(allocation_obj)
        return super().dispatch(request, *args, **kwargs)

    def get_formset_queryset(self):
        queryset = (
            self.allocation.allocationuser_set.exclude(status__name__in=["Removed", "Error"])
            .exclude(user=self.allocation.project.pi)
            .exclude(user=self.request.user)
        )
        return queryset

    def get_formset_factory_kwargs(self):
        kwargs = super().get_formset_factory_kwargs()
        kwargs["formset"] = BaseAllocationUserFormSet
        return kwargs

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        allocation_user_removed_status = AllocationUserStatusChoice.objects.get(name="Removed")
        kwargs.update(
            {
                "action": BaseAllocationUserFormSet.Action.REMOVE,
                "form_kwargs": {"initial": {"status": allocation_user_removed_status}},
            }
        )
        return kwargs

    def formset_valid(self, formset):
        redirect = super().formset_valid(formset)
        allocation_users = self.objects

        for allocation_user in allocation_users:
            allocation_remove_user.send(sender=self.__class__, allocation_user_pk=allocation_user.pk)

        users_removed_count = len(allocation_users)
        messages.success(
            self.request, f"Removed {users_removed_count} user{pluralize(users_removed_count)} from allocation."
        )
        return redirect


class AllocationAttributeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AllocationAttribute
    form_class = AllocationAttributeForm
    template_name = "allocation/allocation_allocationattribute_create.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True
        messages.error(self.request, "You do not have permission to add allocation attributes.")
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allocation"] = self.allocation
        return context

    def get(self, request, *args, **kwargs):
        self.allocation = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.allocation = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["allocation"] = self.allocation
        return initial

    def get_success_url(self):
        # can probably be replaced with `return self.object.allocation.get_absolute_url()`
        return reverse("allocation-detail", kwargs={"pk": self.kwargs.get("pk")})


class AllocationAttributeDeleteView(LoginRequiredMixin, UserPassesTestMixin, AllocationInContextView, ModelFormSetView):
    formset_model = AllocationAttribute
    formset_form_class = AllocationAttributeForm
    formsest_prefix = "attributeform"
    template_name = "allocation/allocation_allocationattribute_delete.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True
        messages.error(self.request, "You do not have permission to delete allocation attributes.")
        return False

    def get_formset_queryset(self):
        return self.allocation.allocationattribute_set.all()

    def get_formset_factory_kwargs(self):
        kwargs = super().get_formset_factory_kwargs()
        kwargs.update(
            {
                "extra": 0,
                "max_num": self.get_formset_queryset().count(),
                "can_delete": True,
            }
        )
        return kwargs

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["form_kwargs"] = {"disabled_fields": ["allocation_attribute_type", "allocation", "value"]}
        return kwargs

    def formset_valid(self, formset):
        formset.save()
        deleted_attributes = formset.deleted_objects

        attributes_deleted_count = len(deleted_attributes)
        messages.success(
            self.request,
            f"Deleted {attributes_deleted_count} attribute{pluralize(attributes_deleted_count)} from allocation.",
        )
        return super().formset_valid(formset)


class AllocationAttributeEditView(LoginRequiredMixin, UserPassesTestMixin, AllocationInContextView, ModelFormSetView):
    formset_model = AllocationAttribute
    formset_form_class = AllocationAttributeForm
    formset_prefix = "attributeform"
    template_name = "allocation/allocation_attribute_edit.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True

        messages.error(self.request, "You do not have permission to edit this allocation's attributes.")

        return False

    def get_allocation_attributes_to_change(self, allocation_obj):
        attributes_to_change = allocation_obj.allocationattribute_set.all()

        attributes_to_change = [
            {
                "attribute_pk": attribute.pk,
                "name": attribute.allocation_attribute_type.name,
                "orig_value": attribute.value,
                "value": attribute.value,
            }
            for attribute in attributes_to_change
        ]

        return attributes_to_change

    def get_formset_queryset(self):
        return self.allocation.allocationattribute_set.all()

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["form_kwargs"] = {"disabled_fields": ["allocation_attribute_type", "allocation"]}
        return kwargs

    def get_formset(self):
        formset = super().get_formset()
        for form in formset:
            form.fields["allocation_attribute_type"].widget = forms.HiddenInput()
        return formset


class AllocationNoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AllocationUserNote
    fields = "__all__"
    template_name = "allocation/allocation_note_create.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True
        messages.error(self.request, "You do not have permission to add allocation notes.")
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)
        context["allocation"] = allocation_obj
        return context

    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)
        author = self.request.user
        initial["allocation"] = allocation_obj
        initial["author"] = author
        return initial

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class)
        form.fields["allocation"].widget = forms.HiddenInput()
        form.fields["author"].widget = forms.HiddenInput()
        form.order_fields(["allocation", "author", "note", "is_private"])
        return form

    def get_success_url(self):
        # can probably be replaced with `return self.object.allocation.get_absolute_url()`
        return reverse("allocation-detail", kwargs={"pk": self.kwargs.get("pk")})


class AllocationRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "allocation/allocation_request_list.html"
    context_object_name = "allocation_list"
    login_url = "/"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_review_allocation_requests"):
            return True

        messages.error(self.request, "You do not have permission to review allocation requests.")
        return False

    def get_queryset(self):
        allocation_list = Allocation.objects.filter(
            status__name__in=[
                "New",
                "Renewal Requested",
                "Paid",
                "Approved",
            ]
        )
        return allocation_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allocation_list = self.get_queryset()

        allocation_renewal_dates = {}
        for allocation in allocation_list.filter(status__name="Renewal Requested"):
            history = allocation.history.order_by("-history_date").first()
            if history.status.name == "Renewal Requested":
                allocation_renewal_dates[allocation.pk] = history.history_date

        context["allocation_renewal_dates"] = allocation_renewal_dates
        context["allocation_status_active"] = AllocationStatusChoice.objects.get(name="Active")
        return context


class AllocationRenewView(LoginRequiredMixin, UserPassesTestMixin, AllocationInContextView, ModelFormSetView):
    formset_model = AllocationUser
    formset_form_class = AllocationReviewUserForm
    template_name = "allocation/allocation_renew.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        if allocation_obj.has_perm(self.request.user, AllocationPermission.MANAGER):
            return True

        messages.error(self.request, "You do not have permission to renew allocation.")
        return False

    def dispatch(self, request, *args, **kwargs):
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        if not ALLOCATION_ENABLE_ALLOCATION_RENEWAL:
            messages.error(
                request,
                "Allocation renewal is disabled. Request a new allocation to this resource if you want to continue using it after the active until date.",
            )
            return redirect(allocation_obj)

        if allocation_obj.status.name not in ["Active"]:
            messages.error(request, f"You cannot renew a allocation with status {allocation_obj.status.name}.")
            return redirect(allocation_obj)

        if allocation_obj.project.needs_review:
            messages.error(request, "You cannot renew your allocation because you have to review your project first.")
            return redirect(allocation_obj.project)

        if allocation_obj.expires_in > 60:
            messages.error(request, "It is too soon to review your allocation.")
            return redirect(allocation_obj)

        return super().dispatch(request, *args, **kwargs)

    def get_formset_queryset(self):
        allocation_users_qs = (
            self.allocation.allocationuser_set.exclude(status__name__in=["Removed"])
            .exclude(user__pk__in=[self.allocation.project.pi.pk, self.request.user.pk])
            .order_by("user__username")
        )
        return allocation_users_qs

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs["form_kwargs"] = {"disabled_fields": ["allocation", "user", "status"]}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.allocation.get_parent_resource.resourceattribute_set.filter(
            resource_attribute_type__name="eula"
        ).exists():
            value = self.allocation.get_parent_resource.resourceattribute_set.get(
                resource_attribute_type__name="eula"
            ).value
            context["resource_eula"] = {"eula": value}

        return context

    def formset_valid(self, formset):
        redirect = super().formset_valid(formset)

        self.allocation.status = AllocationStatusChoice.objects.get(name="Renewal Requested")
        self.allocation.save()

        send_allocation_admin_email(
            self.allocation,
            "Allocation Renewed",
            "email/allocation_renewed.txt",
            domain_url=get_domain_url(self.request),
        )

        messages.success(self.request, "Allocation renewed successfully")
        return redirect


class AllocationInvoiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Allocation
    template_name = "allocation/allocation_invoice_list.html"
    context_object_name = "allocation_list"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_manage_invoice"):
            return True

        messages.error(self.request, "You do not have permission to manage invoices.")
        return False

    def get_queryset(self):
        allocations = Allocation.objects.filter(
            status__name__in=[
                "Paid",
                "Payment Pending",
                "Payment Requested",
                "Payment Declined",
            ]
        )
        return allocations


class AllocationInvoiceDetailView(
    LoginRequiredMixin, UserPassesTestMixin, FormErrorsInMessagesMixin, AllocationInContextView, FormView
):
    form_class = AllocationInvoiceUpdateForm
    template_name = "allocation/allocation_invoice_detail.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_manage_invoice"):
            return True

        messages.error(self.request, "You do not have permission to view invoices.")
        return False

    def get_context_data(self, **kwargs):
        """Create all the variables for allocation_invoice_detail.html"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        allocation_obj = get_object_or_404(Allocation, pk=pk)
        allocation_users = allocation_obj.allocationuser_set.exclude(status__name__in=["Removed"]).order_by(
            "user__username"
        )

        alloc_attr_set = allocation_obj.get_attribute_set(self.request.user)

        attributes_with_usage = [a for a in alloc_attr_set if hasattr(a, "allocationattributeusage")]
        attributes = [a for a in alloc_attr_set]

        guage_data = []
        invalid_attributes = []
        for attribute in attributes_with_usage:
            try:
                guage_data.append(
                    generate_guauge_data_from_usage(
                        attribute.allocation_attribute_type.name,
                        float(attribute.value),
                        float(attribute.allocationattributeusage.value),
                    )
                )
            except ValueError:
                logger.error(
                    "Allocation attribute '%s' is not an int but has a usage", attribute.allocation_attribute_type.name
                )
                invalid_attributes.append(attribute)

        for a in invalid_attributes:
            attributes_with_usage.remove(a)

        context["guage_data"] = guage_data
        context["attributes_with_usage"] = attributes_with_usage
        context["attributes"] = attributes

        # Can the user update the project?
        context["is_allowed_to_update_project"] = allocation_obj.project.has_perm(
            self.request.user, ProjectPermission.UPDATE
        )
        context["allocation_users"] = allocation_users

        if self.request.user.is_superuser:
            notes = allocation_obj.allocationusernote_set.all()
        else:
            notes = allocation_obj.allocationusernote_set.filter(is_private=False)

        context["notes"] = notes
        return context

    def get_initial(self):
        return {"status": self.allocation.status}

    def form_valid(self, form):
        form_data = form.cleaned_data
        self.allocation.status = form_data.get("status")
        self.allocation.save()
        messages.success(self.request, "Allocation updated!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("allocation-invoice-detail", kwargs={"pk": self.allocation.pk})


class AllocationInvoiceNoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AllocationUserNote
    form_class = AllocationInvoiceNoteForm
    template_name = "allocation/allocation_add_invoice_note.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_manage_invoice"):
            return True

        messages.error(self.request, "You do not have permission to manage invoices.")
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        context["allocation"] = allocation_obj
        return context

    def get_initial(self):
        return {
            "author": self.request.user,
            "allocation": get_object_or_404(Allocation, pk=self.kwargs.get("pk")),
        }


class AllocationInvoiceNoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AllocationUserNote
    form_class = AllocationInvoiceNoteForm
    template_name = "allocation/allocation_update_invoice_note.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_manage_invoice"):
            return True

        messages.error(self.request, "You do not have permission to manage invoices.")
        return False


class AllocationInvoiceNoteDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, AllocationInContextView, ModelFormSetView
):
    form_class = AllocationInvoiceNoteForm
    formset_model = AllocationUserNote
    formset_form_class = AllocationInvoiceNoteForm
    formset_prefix = "noteform"
    template_name = "allocation/allocation_delete_invoice_note.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_manage_invoice"):
            return True

        messages.error(self.request, "You do not have permission to manage invoices.")
        return False

    def get_formset_factory_kwargs(self):
        kwargs = super().get_formset_factory_kwargs()
        kwargs["can_delete"] = True
        return kwargs

    def get_formset_queryset(self):
        return self.allocation.allocationusernote_set.all()

    def get_formset(self):
        formset = super().get_formset()
        for form in formset:
            form.fields["note"].widget = forms.HiddenInput()
            form.fields["note"].disabled = True
        return formset

    def get_success_url(self):
        return reverse("allocation-invoice-detail", kwargs={"pk": self.allocation.pk})


class AllocationAccountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # TODO: form_valid and form_invalid set headers... not super sure why
    #       but this is unique compared to the rest of the codebase
    model = AllocationAccount
    template_name = "allocation/allocation_allocationaccount_create.html"
    form_class = AllocationAccountForm

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if not settings.ALLOCATION_ACCOUNT_ENABLED:
            return False
        if self.request.user.is_superuser:
            return True
        if self.request.user.userprofile.is_pi:
            return True

        messages.error(self.request, "You do not have permission to add allocation attributes.")
        return False

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)
        return response

    def get_success_url(self):
        return reverse_lazy("allocation-account-list")


class AllocationAccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AllocationAccount
    template_name = "allocation/allocation_account_list.html"
    context_object_name = "allocationaccount_list"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if not settings.ALLOCATION_ACCOUNT_ENABLED:
            return False
        if self.request.user.is_superuser:
            return True
        if self.request.user.userprofile.is_pi:
            return True

        messages.error(self.request, "You do not have permission to manage invoices.")
        return False

    def get_queryset(self):
        return AllocationAccount.objects.filter(user=self.request.user)


class AllocationChangeDetailView(
    LoginRequiredMixin, UserPassesTestMixin, FormErrorsInMessagesMixin, ModelFormSetView, UpdateView
):
    model = AllocationChangeRequest
    form_class = AllocationChangeRequestForm
    formset_model = AllocationAttributeChangeRequest
    formset_form_class = AllocationAttributeChangeRequestForm
    template_name = "allocation/allocation_change_detail.html"
    context_object_name = "allocation_change"
    formset_prefix = "attributeform"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        allocation_change_obj = get_object_or_404(AllocationChangeRequest, pk=self.kwargs.get("pk"))

        if self.request.user.has_perm("allocation.can_view_all_allocations"):
            return True

        if allocation_change_obj.allocation.has_perm(self.request.user, AllocationPermission.MANAGER):
            return True

        return False

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["disabled_fields"] = ["allocation", "justification", "status"]
        if self.object.status.name != "Pending" or (
            not self.request.user.is_staff and not self.request.user.is_superuser
        ):
            kwargs["disabled_fields"].append("end_date_extension")
        return kwargs

    def get_formset_queryset(self):
        return self.object.allocationattributechangerequest_set.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        redirect = HttpResponseRedirect(reverse("allocation-change-detail", kwargs={"pk": self.object.pk}))
        if not self.request.user.is_superuser:
            messages.error(request, "You do not have permission to update an allocation change request")
            return redirect

        action = request.POST.get("action")
        if action not in ["update", "approve", "deny"]:
            return HttpResponseBadRequest("Invalid request")

        form = self.get_form()
        formset = self.get_formset()

        if not form.is_valid():
            return self.form_invalid(form)

        if action == "deny":
            self.object = form.save()
            allocation_change_status_denied_obj = AllocationChangeStatusChoice.objects.get(name="Denied")
            self.object.status = allocation_change_status_denied_obj
            self.object.save()

            messages.success(
                request,
                "Allocation change request to {} has been DENIED for {} {} ({})".format(
                    self.object.allocation.resources.first(),
                    self.object.allocation.project.pi.first_name,
                    self.object.allocation.project.pi.last_name,
                    self.object.allocation.project.pi.username,
                ),
            )
            send_allocation_customer_email(
                self.object.allocation,
                "Allocation Change Denied",
                "email/allocation_change_denied.txt",
                domain_url=get_domain_url(self.request),
            )

            return redirect

        if not formset.is_valid():
            return self.formset_invalid(formset)

        # formset.clean() checks if the value is the same as the original
        # deleting all the allocation attribute change requests can result in an
        # "invalid" change request
        change_requested = form.has_changed() or (formset and formset.is_valid())
        if not change_requested:
            messages.error(request, "You must make a change to the allocation.")
            return self.formset_invalid(formset)

        if action == "update" and self.object.status.name != "Pending":
            # This is copying the original logic - not sure why only notes gets saved
            # when the change request's status is pending
            self.object.notes = form.cleaned_data.get("notes")
            self.object.save()
            messages.success(request, "Allocation change request updated!")
            return redirect

        self.object = form.save()
        formset.save()

        if action == "update":
            messages.success(request, "Allocation change request updated!")
            return redirect

        if action == "approve":
            # could probably be moved to the allocation change request (like self.object.approve())
            allocation_change_status_active_obj = AllocationChangeStatusChoice.objects.get(name="Approved")
            self.object.status = allocation_change_status_active_obj

            if self.object.end_date_extension > 0:
                new_end_date = self.object.allocation.end_date + relativedelta(days=self.object.end_date_extension)
                self.object.allocation.end_date = new_end_date

                self.object.allocation.save()

            self.object.save()

            for form in formset:
                form_data = form.cleaned_data
                allocation = form_data.get("allocation")
                allocation_attribute = form_data.get("allocation_attribute")
                new_value = form_data.get("new_value")
                allocation_attribute.value = new_value
                allocation_attribute.save()
                allocation_attribute_changed.send(
                    sender=self.__class__,
                    attribute_pk=allocation_attribute.pk,
                    allocation_pk=allocation.pk,
                )

            messages.success(
                request,
                "Allocation change request to {} has been APPROVED for {} {} ({})".format(
                    self.object.allocation.get_parent_resource,
                    self.object.allocation.project.pi.first_name,
                    self.object.allocation.project.pi.last_name,
                    self.object.allocation.project.pi.username,
                ),
            )

            allocation_change_approved.send(
                sender=self.__class__,
                allocation_pk=self.object.allocation.pk,
                allocation_change_pk=self.object.pk,
            )

            send_allocation_customer_email(
                self.object.allocation,
                "Allocation Change Approved",
                "email/allocation_change_approved.txt",
                domain_url=get_domain_url(self.request),
            )

        return redirect


class AllocationChangeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AllocationChangeRequest
    template_name = "allocation/allocation_change_list.html"
    context_object_name = "allocation_change_list"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_review_allocation_requests"):
            return True

        messages.error(self.request, "You do not have permission to review allocation requests.")

        return False

    def get_queryset(self):
        allocation_change_list = AllocationChangeRequest.objects.filter(status__name__in=["Pending"])
        return allocation_change_list


class AllocationChangeView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    FormErrorsInMessagesMixin,
    AllocationInContextView,
    FormView,
    ModelFormSetView,
):
    form_class = AllocationChangeRequestForm
    formset_model = AllocationAttributeChangeRequest
    formset_form_class = AllocationAttributeChangeRequestForm
    template_name = "allocation/allocation_change.html"
    formset_prefix = "attributeform"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))
        if allocation_obj.has_perm(self.request.user, AllocationPermission.MANAGER):
            return True

        messages.error(self.request, "You do not have permission to request changes to this allocation.")

        return False

    def dispatch(self, request, *args, **kwargs):
        allocation_obj = get_object_or_404(Allocation, pk=self.kwargs.get("pk"))

        if allocation_obj.project.needs_review:
            messages.error(
                request, "You cannot request a change to this allocation because you have to review your project first."
            )
            return redirect(allocation_obj)

        if allocation_obj.project.status.name not in [
            "Active",
            "New",
        ]:
            messages.error(request, "You cannot request a change to an allocation in an archived project.")
            return redirect(allocation_obj)

        if allocation_obj.is_locked:
            messages.error(request, "You cannot request a change to a locked allocation.")
            return redirect(allocation_obj)

        if allocation_obj.status.name not in [
            "Active",
            "Renewal Requested",
            "Payment Pending",
            "Payment Requested",
            "Paid",
        ]:
            messages.error(
                request, f'You cannot request a change to an allocation with status "{allocation_obj.status.name}".'
            )
            return redirect(allocation_obj)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["allocation"] = self.allocation
        initial["status"] = AllocationChangeStatusChoice.objects.get(name="Pending")
        return initial

    def get_formset_queryset(self):
        return AllocationAttributeChangeRequest.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["disabled_fields"] = ["allocation", "status", "notes"]
        return kwargs

    def get_formset_initial(self):
        queryset = self.allocation.allocationattribute_set.filter(allocation_attribute_type__is_changeable=True)
        allocation_attributes_to_change = [
            {
                "allocation_change_request": None,
                "allocation_attribute": attribute,
                "new_value": attribute.value,
            }
            for attribute in queryset
        ]
        return allocation_attributes_to_change

    def get_formset(self):
        formset = super().get_formset()
        for form in formset:
            form.fields["allocation_change_request"].required = False
        return formset

    def post(self, request, *args, **kwargs):
        self.allocation = self.get_object()
        self.object = self.allocation

        form = self.get_form()
        formset = self.get_formset()

        change_requested = form.has_changed() or formset.has_changed()
        if not change_requested:
            messages.error(request, "You must request a change.")
            return self.render_to_response(self.get_context_data(form=form))

        if not form.is_valid():
            return self.form_invalid(form)

        if not formset.is_valid():
            return self.formset_invalid(formset)

        # forms are valid
        allocation_change_request = form.save()
        instances = formset.save(commit=False)
        for instance in instances:
            instance.allocation_change_request = allocation_change_request
            instance.save()

        messages.success(request, "Allocation change request successfully submitted.")

        allocation_change_created.send(
            sender=self.__class__,
            allocation_pk=self.allocation.pk,
            allocation_change_pk=allocation_change_request.pk,
        )

        send_allocation_admin_email(
            self.allocation,
            "New Allocation Change Request",
            "email/new_allocation_change_request.txt",
            url_path=reverse("allocation-change-list"),
            domain_url=get_domain_url(self.request),
        )
        return HttpResponseRedirect(self.get_success_url())


class AllocationChangeDeleteAttributeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("allocation.can_review_allocation_requests"):
            return True

        messages.error(self.request, "You do not have permission to update an allocation change request.")
        return False

    def get(self, request, pk):
        allocation_attribute_change_obj = get_object_or_404(AllocationAttributeChangeRequest, pk=pk)
        allocation_change_pk = allocation_attribute_change_obj.allocation_change_request.pk

        allocation_attribute_change_obj.delete()

        messages.success(request, "Allocation attribute change request successfully deleted.")
        return HttpResponseRedirect(reverse("allocation-change-detail", kwargs={"pk": allocation_change_pk}))
