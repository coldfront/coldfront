# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from coldfront.core.project.views.project_add_users_search_views import (
    ProjectAddUsersSearchResultsView,
    ProjectAddUsersSearchView,
)
from coldfront.core.project.views.project_add_users_view import ProjectAddUsersView
from coldfront.core.project.views.project_archive_project_view import ProjectArchiveProjectView
from coldfront.core.project.views.project_archived_list_view import ProjectArchivedListView
from coldfront.core.project.views.project_attribute_views import (
    ProjectAttributeCreateView,
    ProjectAttributeDeleteView,
    ProjectAttributeUpdateView,
)
from coldfront.core.project.views.project_create_update_views import ProjectCreateView, ProjectUpdateView
from coldfront.core.project.views.project_detail_view import ProjectDetailView
from coldfront.core.project.views.project_list_view import ProjectListView
from coldfront.core.project.views.project_note_create_view import ProjectNoteCreateView
from coldfront.core.project.views.project_remove_users_view import ProjectRemoveUsersView
from coldfront.core.project.views.project_review_views import (
    ProjectReviewCompleteView,
    ProjectReviewEmailView,
    ProjectReviewListView,
    ProjectReviewView,
)
from coldfront.core.project.views.project_update_email_notification_view import project_update_email_notification
from coldfront.core.project.views.project_user_detail_view import ProjectUserDetail

__all__ = [
    "ProjectAddUsersSearchResultsView",
    "ProjectAddUsersSearchView",
    "ProjectAddUsersView",
    "ProjectArchiveProjectView",
    "ProjectAttributeCreateView",
    "ProjectAttributeDeleteView",
    "ProjectAttributeUpdateView",
    "ProjectCreateView",
    "ProjectDetailView",
    "ProjectListView",
    "ProjectNoteCreateView",
    "ProjectRemoveUsersView",
    "ProjectReviewCompleteView",
    "ProjectReviewEmailView",
    "ProjectReviewListView",
    "ProjectReviewView",
    "project_update_email_notification",
    "ProjectUpdateView",
    "ProjectUserDetail",
    "ProjectArchivedListView",
]
