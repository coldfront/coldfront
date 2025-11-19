# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from .project_add_users_search_views import ProjectAddUsersSearchResultsView, ProjectAddUsersSearchView
from .project_add_users_view import ProjectAddUsersView
from .project_archive_project_view import ProjectArchiveProjectView
from .project_archived_list_view import ProjectArchivedListView
from .project_attribute_views import ProjectAttributeCreateView, ProjectAttributeDeleteView, ProjectAttributeUpdateView
from .project_create_update_views import ProjectCreateView, ProjectUpdateView
from .project_detail_view import ProjectDetailView
from .project_list_view import ProjectListView
from .project_note_create_view import ProjectNoteCreateView
from .project_remove_users_view import ProjectRemoveUsersView
from .project_review_views import (
    ProjectReviewCompleteView,
    ProjectReviewEmailView,
    ProjectReviewListView,
    ProjectReviewView,
)
from .project_update_email_notification_view import project_update_email_notification
from .project_user_detail_view import ProjectUserDetail

__all__ = [
    "ProjectAddUsersSearchView",
    "ProjectAddUsersSearchResultsView",
    "ProjectAddUsersView",
    "ProjectArchiveProjectView",
    "ProjectArchivedListView",
    "ProjectAttributeCreateView",
    "ProjectAttributeDeleteView",
    "ProjectAttributeUpdateView",
    "ProjectCreateView",
    "ProjectUpdateView",
    "ProjectDetailView",
    "ProjectListView",
    "ProjectNoteCreateView",
    "ProjectRemoveUsersView",
    "ProjectReviewView",
    "ProjectReviewListView",
    "ProjectReviewCompleteView",
    "ProjectReviewEmailView",
    "ProjectUserDetail",
    "project_update_email_notification",
]
