# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.apps import apps


def get_missing_bridge_models(allocation):
    """
    Return a list of bridge model classes that are required by the
    allocation's resource but don't exist yet.

    Each resource model can declare ``required_bridge_models`` as a
    tuple of ``"app_label.ModelName"`` strings.  For each entry, we
    check whether at least one instance with ``allocation=allocation``
    exists.  Missing models are returned as model classes (usable with
    ``{% action_url %}`` in templates).
    """
    resource = allocation.resource_object
    if resource is None:
        return []

    missing = []
    # allocation must be saved (have a pk) to filter by FK
    if not allocation.pk:
        return missing
    for model_path in getattr(resource, "required_bridge_models", ()):
        app_label, model_name = model_path.split(".", 1)
        model = apps.get_model(app_label, model_name)
        if model is None:
            continue
        # Bridge models should have an ``allocation`` FK to the Allocation
        # model.  Check existence via that relation.
        if not model.objects.filter(allocation=allocation).exists():
            missing.append(model)
    return missing
