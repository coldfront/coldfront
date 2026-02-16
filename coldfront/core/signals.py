# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from coldfront.core.models import ObjectType


@receiver(post_migrate)
def update_object_types(sender, **kwargs):
    """
    Create or update the corresponding ObjectType for each model within the migrated app.
    """
    for model in sender.get_models():
        app_label, model_name = model._meta.label_lower.split(".")

        # Determine whether model is public and its supported features
        is_public = ObjectType.model_is_public(model)
        features = ObjectType.get_model_features(model)

        # Create/update the ObjectType for the model
        try:
            ot = ObjectType.objects.get_by_natural_key(app_label=app_label, model=model_name)
            ot.public = is_public
            ot.features = features
            ot.save()
        except ObjectDoesNotExist:
            ObjectType.objects.create(
                app_label=app_label,
                model=model_name,
                public=is_public,
                features=features,
            )
