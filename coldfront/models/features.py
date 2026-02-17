# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import json

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

from coldfront.core.choices import ObjectChangeActionChoices
from coldfront.core.models.change_logging import ObjectChange
from coldfront.core.utils import is_taggable
from coldfront.registry import register_model_feature
from coldfront.utils.serialization import serialize_object

from .deletion import DeleteMixin


class ChangeLoggingMixin(DeleteMixin, models.Model):
    """
    Provides change logging support for a model. Adds the `created` and `last_updated` fields.
    """

    created = models.DateTimeField(
        verbose_name=_("created"),
        auto_now_add=True,
        blank=True,
        null=True,
    )
    last_updated = models.DateTimeField(
        verbose_name=_("last updated"),
        auto_now=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        changelog_message = kwargs.pop("changelog_message", None)
        super().__init__(*args, **kwargs)
        self._changelog_message = changelog_message

    def serialize_object(self, exclude=None):
        """
        Return a JSON representation of the instance. Models can override this method to replace or extend the default
        serialization logic provided by the `serialize_object()` utility function.

        Args:
            exclude: An iterable of attribute names to omit from the serialized output
        """
        return serialize_object(self, exclude=exclude or [])

    def snapshot(self):
        """
        Save a snapshot of the object's current state in preparation for modification. The snapshot is saved as
        `_prechange_snapshot` on the instance.
        """
        exclude_fields = []
        if settings.CHANGELOG_SKIP_EMPTY_CHANGES:
            exclude_fields = [
                "last_updated",
            ]

        self._prechange_snapshot = self.serialize_object(exclude=exclude_fields)

    snapshot.alters_data = True

    def to_objectchange(self, action):
        """
        Return a new ObjectChange representing a change made to this object. This will typically be called automatically
        by ChangeLoggingMiddleware.
        """

        exclude = []
        if settings.CHANGELOG_SKIP_EMPTY_CHANGES:
            exclude = ["last_updated"]

        objectchange = ObjectChange(
            changed_object=self,
            object_repr=str(self)[:200],
            action=action,
            message=self._changelog_message or "",
        )
        if hasattr(self, "_prechange_snapshot"):
            objectchange.prechange_data = self._prechange_snapshot
        if action in (ObjectChangeActionChoices.ACTION_CREATE, ObjectChangeActionChoices.ACTION_UPDATE):
            self._postchange_snapshot = self.serialize_object(exclude=exclude)
            objectchange.postchange_data = self._postchange_snapshot

        return objectchange

    to_objectchange.alters_data = True


class CloningMixin(models.Model):
    """
    Provides the clone() method used to prepare a copy of existing objects.
    """

    class Meta:
        abstract = True

    def clone(self):
        """
        Returns a dictionary of attributes suitable for creating a copy of the current instance. This is used for pre-
        populating an object creation form in the UI. By default, this method will replicate any fields listed in the
        model's `clone_fields` list (if defined), but it can be overridden to apply custom logic.

        ```python
        class MyModel(ColdFrontModel):
            def clone(self):
                attrs = super().clone()
                attrs["extra-value"] = 123
                return attrs
        ```
        """
        attrs = {}

        for field_name in getattr(self, "clone_fields", []):
            field = self._meta.get_field(field_name)
            field_value = field.value_from_object(self)
            if field_value and isinstance(field, models.ManyToManyField):
                attrs[field_name] = [v.pk for v in field_value]
            elif field_value and isinstance(field, models.JSONField):
                attrs[field_name] = json.dumps(field_value)
            elif field_value not in (None, ""):
                attrs[field_name] = field_value

        # Handle GenericForeignKeys. If the CT and ID fields are being cloned, also
        # include the name of the GFK attribute itself, as this is what forms expect.
        for field in self._meta.private_fields:
            if isinstance(field, GenericForeignKey):
                if field.ct_field in attrs and field.fk_field in attrs:
                    attrs[field.name] = attrs[field.fk_field]

        # Include tags (if applicable)
        if is_taggable(self):
            attrs["tags"] = [tag.pk for tag in self.tags.all()]

        # Include any cloneable custom fields
        if hasattr(self, "custom_fields"):
            for field in self.custom_fields:
                if field.is_cloneable:
                    attrs[f"cf_{field.name}"] = self.custom_field_data.get(field.name)

        return attrs


register_model_feature("cloning", lambda model: issubclass(model, CloningMixin))
register_model_feature("change_logging", lambda model: issubclass(model, ChangeLoggingMixin))
