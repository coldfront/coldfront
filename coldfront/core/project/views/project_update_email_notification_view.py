# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from coldfront.core.project.models import ProjectUser


@login_required
def project_update_email_notification(request):
    if request.method == "POST":
        data = request.POST
        project_user_obj = get_object_or_404(ProjectUser, pk=data.get("user_project_id"))

        project_obj = project_user_obj.project

        allowed = False
        if project_obj.pi == request.user:
            allowed = True

        if project_obj.projectuser_set.filter(user=request.user, role__name="Manager", status__name="Active").exists():
            allowed = True

        if project_user_obj.user == request.user:
            allowed = True

        if request.user.is_superuser:
            allowed = True

        if allowed is False:
            return HttpResponse("not allowed", status=403)
        else:
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
        return HttpResponse("no POST", status=400)
