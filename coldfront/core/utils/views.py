# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View


class FormErrorsInMessagesMixin:
    """Renders form errors in messages."""

    def form_invalid(self, form):
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors())
        for error in form.errors:
            if error == "__all__":
                continue
            messages.error(self.request, error)
        return super().form_invalid(form)


class FormSetMixin(ContextMixin):
    """Provide a way to show and handle a form in a request."""

    initial = []
    formset_form_class = None
    success_url = None
    formset_prefix = None

    def get_formset_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_formset_prefix(self):
        """Return the prefix to use for forms."""
        return self.formset_prefix

    def get_formset_form_class(self):
        """Return the form class to use when instantiating the formset factory."""
        return self.formset_form_class

    def get_formset(self):
        """Return an instance of the formset to be used in this view."""
        FormSetFactory = formset_factory(**self.get_formset_factory_kwargs())
        return FormSetFactory(**self.get_formset_kwargs())

    def get_formset_factory_kwargs(self):
        """Return the keyword arguments for instantiating the formset factory."""
        initial_len = len(self.get_formset_initial())
        kwargs = {
            "form": self.get_formset_form_class(),
            "extra": initial_len,
            "max_num": initial_len,
        }
        return kwargs

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the formset."""
        kwargs = {
            "initial": self.get_formset_initial(),
            "prefix": self.get_formset_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

    def formset_valid(self, formset):
        """If the formset is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        """If the formset is invalid, render the invalid formset."""
        if formset.non_form_errors():
            messages.error(self.request, formset.non_form_errors())
        for error in formset.errors:
            if error == "__all__":
                continue
            messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_context_data(self, **kwargs):
        if "formset" not in kwargs:
            kwargs["formset"] = self.get_formset()
        return super().get_context_data(**kwargs)


class ModelFormSetMixin(FormSetMixin):
    """Provide a way to show and handle a ModelFormSet in a request."""

    formset_model = None
    formset_queryset = None

    def get_formset_queryset(self):
        """
        Return the list of items for this modelformset.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.formset_queryset is not None:
            queryset = self.formset_queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.formset_model is not None:
            queryset = self.formset_model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )

    def get_formset(self):
        """Return an instance of the formset to be used in this view."""
        ModelFormSetFactory = modelformset_factory(**self.get_formset_factory_kwargs())
        return ModelFormSetFactory(**self.get_formset_kwargs())

    def get_formset_factory_kwargs(self):
        kwargs = super().get_formset_factory_kwargs()
        initial_len = len(self.get_formset_initial())
        queryset_len = self.get_formset_queryset().count()
        kwargs.update(
            {
                "model": self.formset_model,
                "max_num": initial_len + queryset_len,
            }
        )
        return kwargs

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the formset."""
        kwargs = super().get_formset_kwargs()
        kwargs.update({"queryset": self.get_formset_queryset()})
        return kwargs

    def formset_valid(self, formset):
        """If the formset is valid, save the associated formset."""
        self.objects = formset.save()
        return super().formset_valid(formset)


class ProcessFormSetView(View):
    """Render a formset on GET and processes it on POST."""

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the formset."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a formset instance with the passed
        POST variables and then check if it's valid.
        """
        formset = self.get_formset()
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormSetView(FormSetMixin, ProcessFormSetView):
    """A base view for displaying a formset."""


class FormSetView(TemplateResponseMixin, BaseFormSetView):
    """A view for displaying a formset and rendering a template response."""


class BaseModelFormSetView(ModelFormSetMixin, ProcessFormSetView):
    """A base view for displaying a modelformset."""


class ModelFormSetView(TemplateResponseMixin, BaseModelFormSetView):
    """A view for displaying a modelformset and rendering a template response."""
