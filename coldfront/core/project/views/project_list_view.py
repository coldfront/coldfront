# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.views.generic import ListView

from coldfront.core.project.forms import ProjectSearchForm
from coldfront.core.project.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project/project_list.html"
    prefetch_related = [
        "pi",
        "status",
        "field_of_science",
    ]
    context_object_name = "project_list"
    paginate_by = 25

    def get_queryset(self):
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "asc")
        if order_by != "name":
            if direction == "asc":
                direction = ""
            if direction == "des":
                direction = "-"
            order_by = direction + order_by

        project_search_form = ProjectSearchForm(self.request.GET)

        projects = Project.objects.prefetch_related("pi", "field_of_science", "status")

        if project_search_form.is_valid():
            data = project_search_form.cleaned_data
            if data.get("show_all_projects") and (
                self.request.user.is_superuser or self.request.user.has_perm("project.can_view_all_projects")
            ):
                projects = (
                    Project.objects.select_related(
                        "pi",
                        "field_of_science",
                        "status",
                    )
                    .filter(
                        status__name__in=[
                            "New",
                            "Active",
                        ]
                    )
                    .order_by(order_by)
                )
            else:
                projects = (
                    Project.objects.select_related(
                        "pi",
                        "field_of_science",
                        "status",
                    )
                    .filter(
                        Q(
                            status__name__in=[
                                "New",
                                "Active",
                            ]
                        )
                        & Q(projectuser__user=self.request.user)
                        & Q(projectuser__status__name="Active")
                    )
                    .order_by(order_by)
                )

            # Last Name
            if data.get("title"):
                projects = projects.filter(title__icontains=data.get("title"))

            # Last Name
            if data.get("last_name"):
                projects = projects.filter(pi__last_name__icontains=data.get("last_name"))

            # Username
            if data.get("username"):
                projects = projects.filter(
                    Q(pi__username__icontains=data.get("username"))
                    | Q(projectuser__user__username__icontains=data.get("username"))
                    & Q(projectuser__status__name="Active")
                )

            # Field of Science
            if data.get("field_of_science"):
                projects = projects.filter(field_of_science__description__icontains=data.get("field_of_science"))

        else:
            projects = (
                Project.objects.select_related(
                    "pi",
                    "field_of_science",
                    "status",
                )
                .filter(
                    Q(
                        status__name__in=[
                            "New",
                            "Active",
                        ]
                    )
                    & Q(projectuser__user=self.request.user)
                    & Q(projectuser__status__name="Active")
                )
                .order_by(order_by)
            )

        return projects.order_by(order_by).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects_count = self.get_queryset().count()
        context["projects_count"] = projects_count

        project_search_form = ProjectSearchForm(self.request.GET)
        if project_search_form.is_valid():
            context["project_search_form"] = project_search_form
            data = project_search_form.cleaned_data
            filter_parameters = ""
            for key, value in data.items():
                if value:
                    if isinstance(value, list):
                        for ele in value:
                            filter_parameters += "{}={}&".format(key, ele)
                    else:
                        filter_parameters += "{}={}&".format(key, value)
            context["project_search_form"] = project_search_form
        else:
            filter_parameters = None
            context["project_search_form"] = ProjectSearchForm()

        order_by = self.request.GET.get("order_by")
        if order_by:
            direction = self.request.GET.get("direction")
            filter_parameters_with_order_by = filter_parameters + "order_by=%s&direction=%s&" % (order_by, direction)
        else:
            filter_parameters_with_order_by = filter_parameters

        if filter_parameters:
            context["expand_accordion"] = "show"

        context["filter_parameters"] = filter_parameters
        context["filter_parameters_with_order_by"] = filter_parameters_with_order_by

        project_list = context.get("project_list")
        paginator = Paginator(project_list, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            project_list = paginator.page(page)
        except PageNotAnInteger:
            project_list = paginator.page(1)
        except EmptyPage:
            project_list = paginator.page(paginator.num_pages)

        return context
