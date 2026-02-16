# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import collections

from django.utils.translation import gettext as _


class Registry(dict):
    """
    Central registry for registration of functionality. Once a Registry is initialized, keys cannot be added or
    removed (though the value of each key is mutable).
    """

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise KeyError(_("Invalid store: {key}").format(key=key))

    def __setitem__(self, key, value):
        raise TypeError(_("Cannot add stores to registry after initialization"))

    def __delitem__(self, key):
        raise TypeError(_("Cannot delete stores from registry"))


# Initialize the global registry
registry = Registry(
    {
        "model_features": dict(),
        "plugins": dict(),
        "views": collections.defaultdict(dict),
    }
)


def register_model_feature(name, func=None):
    """
    Register a model feature with its qualifying function.

    The qualifying function must accept a single `model` argument. It will be called to determine whether the given
    model supports the corresponding feature.

    This function can be used directly:

        register_model_feature('my_feature', my_func)

    Or as a decorator:

        @register_model_feature('my_feature')
        def my_func(model):
            ...
    """

    def decorator(f):
        registry["model_features"][name] = f
        return f

    if name in registry["model_features"]:
        raise ValueError(f"A model feature named {name} is already registered.")

    if func is None:
        return decorator
    return decorator(func)


def register_model_view(model, name="", path=None, detail=True, kwargs=None):
    """
    This decorator can be used to "attach" a view to any model in ColdFront. This is typically used to inject
    additional tabs within a model's detail view. For example, to add a custom tab to ColdFront's ras.Allocation model:

        @register_model_view(Allocation, 'myview', path='my-custom-view')
        class MyView(ObjectView):
            ...

    This will automatically create a URL path for MyView at `/ras/allocations/<id>/my-custom-view/` which can be
    resolved using the view name `ras:allocation_myview'.

    Args:
        model: The Django model class with which this view will be associated.
        name: The string used to form the view's name for URL resolution (e.g. via `reverse()`). This will be appended
            to the name of the base view for the model using an underscore. If blank, the model name will be used.
        path: The URL path by which the view can be reached (optional). If not provided, `name` will be used.
        detail: True if the path applied to an individual object; False if it attaches to the base (list) path.
        kwargs: A dictionary of keyword arguments for the view to include when registering its URL path (optional).
    """

    def _wrapper(cls):
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        if model_name not in registry["views"][app_label]:
            registry["views"][app_label][model_name] = []

        registry["views"][app_label][model_name].append(
            {
                "name": name,
                "view": cls,
                "path": path if path is not None else name,
                "detail": detail,
                "kwargs": kwargs or {},
            }
        )

        return cls

    return _wrapper


def register_models(*models):
    """
    Register one or more models in ColdFront. This entails:

     - Determining whether the model is considered "public" (available for reference by other models)
     - Registering which features the model supports (e.g. bookmarks, custom fields, etc.)
     - Registering any feature-specific views for the model (e.g. ObjectJournalView instances)

    register_model() should be called for each relevant model under the ready() of an app's AppConfig class.
    """
    for model in models:
        app_label, model_name = model._meta.label_lower.split(".")

        # Register applicable feature views for the model
