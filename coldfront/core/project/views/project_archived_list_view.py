# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from coldfront.core.project.models import Project
from coldfront.core.project.views.project_list_view import ProjectListView

logger = logging.getLogger(__name__)


class ProjectArchivedListView(ProjectListView):
    model = Project
    template_name = "project/project_archived_list.html"
    context_object_name = "project_list"
    paginate_by = 10
    project_status_choices = ["Archived"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expand"] = False
        return context
