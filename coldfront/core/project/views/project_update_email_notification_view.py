# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from coldfront.core.project.models import ProjectUser
from coldfront.core.project.utils import user_is_pi_or_manager


@login_required
def project_update_email_notification(request):
    if request.method == "POST":
        data = request.POST
        project_user_obj = get_object_or_404(ProjectUser, pk=data.get("user_project_id"))
        project_obj = project_user_obj.project

        if user_is_pi_or_manager(request.user, project_obj) or project_user_obj.user == request.user:
            checked = data.get("checked")
            if checked == "true":
                project_user_obj.enable_notifications = True
                project_user_obj.save()
                return HttpResponse("checked", status=200)
            elif checked == "false":
                project_user_obj.enable_notifications = False
                project_user_obj.save()
                return HttpResponse("unchecked", status=200)
            else:
                return HttpResponse("no checked", status=400)
        else:
            return HttpResponse("not allowed", status=403)
    else:
        return HttpResponse("no POST", status=400)
