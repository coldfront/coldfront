# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):
    template_name = "home.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {},
        )


class ObjectSelectorView(LoginRequiredMixin, View):
    template_name = "generic/object_selector.html"

    def get(self, request):
        model = self._get_model(request.GET.get("_model", ""))

        form_class = self._get_form_class(model)
        form = form_class(request.GET)

        if "_search" in request.GET:
            # Return only search results
            filterset = self._get_filterset_class(model)

            queryset = model.objects.restrict(request.user)
            if filterset:
                queryset = filterset(request.GET, queryset, request=request).qs

            return render(
                request,
                "generic/object_selector_results.html",
                {
                    "results": queryset[:100],
                },
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "model": model,
                "target_id": request.GET.get("target"),
            },
        )

    def _get_model(self, label):
        try:
            app_label, model_name = label.split(".")
            content_type = ContentType.objects.get_by_natural_key(app_label, model_name)
        except (ValueError, ObjectDoesNotExist):
            raise Http404
        return content_type.model_class()

    def _get_form_class(self, model):
        if hasattr(self, "form_class"):
            return self.form_class
        app_label = model._meta.app_label
        class_name = f"{model.__name__}FilterSetForm"
        return import_string(f"coldfront.{app_label}.forms.{class_name}")

    def _get_filterset_class(self, model):
        if hasattr(self, "filterset_class"):
            return self.filterset_class
        app_label = model._meta.app_label
        class_name = f"{model.__name__}FilterSet"
        return import_string(f"coldfront.{app_label}.filtersets.{class_name}")
