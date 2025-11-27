# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from coldfront.core.project.forms import (
    ProjectAttributeAddForm,
    ProjectAttributeDeleteForm,
    ProjectAttributeUpdateForm,
)
from coldfront.core.project.models import (
    Project,
    ProjectAttribute,
)
from coldfront.core.project.utils import get_project_attributes, project_is_archived, user_is_pi_or_manager

logger = logging.getLogger(__name__)


class ProjectAttributeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProjectAttribute
    form_class = ProjectAttributeAddForm
    template_name = "project/project_attribute_create.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        has_permission = user_is_pi_or_manager(self.request.user, project_obj)
        if not has_permission:
            messages.error(self.request, "You do not have permission to add project attributes.")
        return has_permission

    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get("pk")
        initial["project"] = get_object_or_404(Project, pk=pk)
        initial["user"] = self.request.user
        return initial

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class)
        form.fields["project"].widget = forms.HiddenInput()
        return form

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        context = super().get_context_data(*args, **kwargs)
        context["project"] = get_object_or_404(Project, pk=pk)
        return context

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.project_id})


class ProjectAttributeDeleteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = ProjectAttribute
    form_class = ProjectAttributeDeleteForm
    template_name = "project/project_attribute_delete.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        has_permission = user_is_pi_or_manager(self.request.user, project_obj)
        if not has_permission:
            messages.error(self.request, "You do not have permission to add project attributes.")
        return has_permission

    def get_avail_attrs(self, project_obj):
        avail_attrs = get_project_attributes(project_obj, show_private=self.request.user.is_superuser)
        return [
            {"pk": attr.pk, "selected": False, "name": str(attr.proj_attr_type), "value": attr.value}
            for attr in avail_attrs
        ]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        project_obj = get_object_or_404(Project, pk=pk)

        project_attributes_to_delete = self.get_avail_attrs(project_obj)
        context = {}

        if project_attributes_to_delete:
            formset = formset_factory(ProjectAttributeDeleteForm, max_num=len(project_attributes_to_delete))
            formset = formset(initial=project_attributes_to_delete, prefix="attributeform")
            context["formset"] = formset
        context["project"] = project_obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        attr_to_delete = self.get_avail_attrs(pk)

        formset = formset_factory(ProjectAttributeDeleteForm, max_num=len(attr_to_delete))
        formset = formset(request.POST, initial=attr_to_delete, prefix="attributeform")

        attributes_deleted_count = 0

        if formset.is_valid():
            for form in formset:
                form_data = form.cleaned_data
                if form_data["selected"]:
                    attributes_deleted_count += 1
                    proj_attr = ProjectAttribute.objects.get(pk=form_data["pk"])
                    proj_attr.delete()

            messages.success(request, "Deleted {} attributes from project.".format(attributes_deleted_count))
        else:
            for error in formset.errors:
                messages.error(request, error)

        return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": pk}))


class ProjectAttributeUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_attribute_update.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        has_permission = user_is_pi_or_manager(self.request.user, project_obj)
        if not has_permission:
            messages.error(self.request, "You do not have permission to update project attributes.")
        return has_permission

    def get(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        project_attribute_pk = self.kwargs.get("project_attribute_pk")

        if project_obj.projectattribute_set.filter(pk=project_attribute_pk).exists():
            project_attribute_obj = project_obj.projectattribute_set.get(pk=project_attribute_pk)

            project_attribute_update_form = ProjectAttributeUpdateForm(
                initial={
                    "pk": self.kwargs.get("project_attribute_pk"),
                    "name": project_attribute_obj,
                    "value": project_attribute_obj.value,
                    "type": project_attribute_obj.proj_attr_type,
                }
            )

            context = {}
            context["project_obj"] = project_obj
            context["project_attribute_update_form"] = project_attribute_update_form
            context["project_attribute_obj"] = project_attribute_obj

            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        project_attribute_pk = self.kwargs.get("project_attribute_pk")

        if project_obj.projectattribute_set.filter(pk=project_attribute_pk).exists():
            project_attribute_obj = project_obj.projectattribute_set.get(pk=project_attribute_pk)

            if project_is_archived(project_obj):
                messages.error(request, "You cannot update an attribute in an archived project.")
                return HttpResponseRedirect(
                    reverse(
                        "project-attribute-update",
                        kwargs={"pk": project_obj.pk, "project_attribute_pk": project_attribute_obj.pk},
                    )
                )

            project_attribute_update_form = ProjectAttributeUpdateForm(
                request.POST,
                initial={"pk": self.kwargs.get("project_attribute_pk")},
            )

            if project_attribute_update_form.is_valid():
                form_data = project_attribute_update_form.cleaned_data
                project_attribute_obj.value = form_data.get("new_value")
                project_attribute_obj.save()

                messages.success(request, "Attribute Updated.")
                return HttpResponseRedirect(reverse("project-detail", kwargs={"pk": project_obj.pk}))
            else:
                for error in project_attribute_update_form.errors.values():
                    messages.error(request, error)
                return HttpResponseRedirect(
                    reverse(
                        "project-attribute-update",
                        kwargs={"pk": project_obj.pk, "project_attribute_pk": project_attribute_obj.pk},
                    )
                )
