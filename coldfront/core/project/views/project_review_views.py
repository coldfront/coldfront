# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from coldfront.core.project.forms import ProjectReviewEmailForm, ProjectReviewForm
from coldfront.core.project.models import Project, ProjectReview, ProjectReviewStatusChoice
from coldfront.core.utils.common import get_domain_url, import_from_settings
from coldfront.core.utils.mail import send_email, send_email_template

EMAIL_ENABLED = import_from_settings("EMAIL_ENABLED", False)
if EMAIL_ENABLED:
    EMAIL_DIRECTOR_EMAIL_ADDRESS = import_from_settings("EMAIL_DIRECTOR_EMAIL_ADDRESS")
    EMAIL_SENDER = import_from_settings("EMAIL_SENDER")


class ProjectReviewView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "project/project_review.html"
    login_url = "/"  # redirect URL if fail test_func

    def test_func(self):
        """UserPassesTestMixin Tests"""
        if self.request.user.is_superuser:
            return True

        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if project_obj.pi == self.request.user:
            return True

        if project_obj.projectuser_set.filter(
            user=self.request.user, role__name="Manager", status__name="Active"
        ).exists():
            return True

        messages.error(self.request, "You do not have permissions to review this project.")

    def dispatch(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if not project_obj.needs_review:
            messages.error(request, "You do not need to review this project.")
            return redirect(project_obj)

        if "Auto-Import Project".lower() in project_obj.title.lower():
            messages.error(
                request,
                'You must update the project title before reviewing your project. You cannot have "Auto-Import Project" in the title.',
            )
            return HttpResponseRedirect(reverse("project-update", kwargs={"pk": project_obj.pk}))

        if (
            "We do not have information about your research. Please provide a detailed description of your work and update your field of science. Thank you!"
            in project_obj.description
        ):
            messages.error(request, "You must update the project description before reviewing your project.")
            return HttpResponseRedirect(reverse("project-update", kwargs={"pk": project_obj.pk}))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        project_review_form = ProjectReviewForm(project_obj.pk)

        context = {}
        context["project"] = project_obj
        context["project_review_form"] = project_review_form
        context["project_users"] = ", ".join(
            [
                "{} {}".format(ele.user.first_name, ele.user.last_name)
                for ele in project_obj.projectuser_set.filter(status__name="Active").order_by("user__last_name")
            ]
        )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        project_obj = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        project_review_form = ProjectReviewForm(project_obj.pk, request.POST)

        project_review_status_choice = ProjectReviewStatusChoice.objects.get(name="Pending")

        if project_review_form.is_valid():
            form_data = project_review_form.cleaned_data
            project_review_obj = ProjectReview.objects.create(
                project=project_obj,
                reason_for_not_updating_project=form_data.get("reason"),
                status=project_review_status_choice,
            )

            project_obj.force_review = False
            project_obj.save()

            domain_url = get_domain_url(self.request)
            project_review_list_url = "{}{}".format(domain_url, reverse("project-review-list"))
            project_url = "{}{}".format(domain_url, project_obj.get_absolute_url())

            email_context = {
                "project": project_obj,
                "project_url": project_url,
                "project_review": project_review_obj,
                "project_review_list_url": project_review_list_url,
            }

            if EMAIL_ENABLED:
                send_email_template(
                    "New project review has been submitted",
                    "email/new_project_review.txt",
                    email_context,
                    EMAIL_SENDER,
                    [
                        EMAIL_DIRECTOR_EMAIL_ADDRESS,
                    ],
                )

            messages.success(request, "Project reviewed successfully.")
            return redirect(project_obj)
        else:
            messages.error(request, "There was an error in processing  your project review.")
            return redirect(project_obj)


class ProjectReviewListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ProjectReview
    template_name = "project/project_review_list.html"
    prefetch_related = [
        "project",
    ]
    context_object_name = "project_review_list"

    def get_queryset(self):
        return ProjectReview.objects.filter(status__name="Pending")

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("project.can_review_pending_project_reviews"):
            return True

        messages.error(self.request, "You do not have permission to review pending project reviews.")


class ProjectReviewCompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("project.can_review_pending_project_reviews"):
            return True

        messages.error(self.request, "You do not have permission to mark a pending project review as completed.")

    def get(self, request, project_review_pk):
        project_review_obj = get_object_or_404(ProjectReview, pk=project_review_pk)

        project_review_status_completed_obj = ProjectReviewStatusChoice.objects.get(name="Completed")
        project_review_obj.status = project_review_status_completed_obj
        project_review_obj.project.project_needs_review = False
        project_review_obj.save()

        messages.success(request, "Project review for {} has been completed".format(project_review_obj.project.title))

        return HttpResponseRedirect(reverse("project-review-list"))


class ProjectReviewEmailView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ProjectReviewEmailForm
    template_name = "project/project_review_email.html"
    login_url = "/"

    def test_func(self):
        """UserPassesTestMixin Tests"""

        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm("project.can_review_pending_project_reviews"):
            return True

        messages.error(self.request, "You do not have permission to send email for a pending project review.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        project_review_obj = get_object_or_404(ProjectReview, pk=pk)
        context["project_review"] = project_review_obj

        return context

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.kwargs.get("pk"), **self.get_form_kwargs())

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        project_review_obj = get_object_or_404(ProjectReview, pk=pk)
        form_data = form.cleaned_data

        receiver_list = [project_review_obj.project.pi.email]
        cc = form_data.get("cc").strip()
        if cc:
            cc = cc.split(",")
        else:
            cc = []

        send_email(
            "Request for more information", form_data.get("email_body"), EMAIL_DIRECTOR_EMAIL_ADDRESS, receiver_list, cc
        )

        messages.success(
            self.request,
            "Email sent to {} {} ({})".format(
                project_review_obj.project.pi.first_name,
                project_review_obj.project.pi.last_name,
                project_review_obj.project.pi.username,
            ),
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project-review-list")
