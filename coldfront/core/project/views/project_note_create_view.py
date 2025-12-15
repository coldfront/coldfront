# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from coldfront.core.project.models import Project, ProjectUserMessage


class ProjectNoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProjectUserMessage
    fields = "__all__"
    template_name = "project/project_note_create.html"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True
        else:
            messages.error(self.request, "You do not have permission to add project notes.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        project_obj = get_object_or_404(Project, pk=pk)
        context["project"] = project_obj
        return context

    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get("pk")
        project_obj = get_object_or_404(Project, pk=pk)
        author = self.request.user
        initial["project"] = project_obj
        initial["author"] = author
        return initial

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class)
        form.fields["project"].widget = forms.HiddenInput()
        form.fields["author"].widget = forms.HiddenInput()
        form.order_fields(["project", "author", "message", "is_private"])
        return form

    def get_success_url(self):
        # can probably be replaced with `return self.object.project.get_aboslute_url()`
        return reverse("project-detail", kwargs={"pk": self.kwargs.get("pk")})
