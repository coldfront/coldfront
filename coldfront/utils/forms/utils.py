# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0


from coldfront.users.querysets import RestrictedQuerySet


def add_blank_choice(choices):
    """
    Add a blank choice to the beginning of a choices list.
    """
    return ((None, "---------"),) + tuple(choices)


def restrict_form_fields(form, user, action="view"):
    """
    Restrict all form fields which reference a RestrictedQuerySet. This ensures that users see only permitted objects
    as available choices.
    """
    for field in form.fields.values():
        if hasattr(field, "queryset") and issubclass(field.queryset.__class__, RestrictedQuerySet):
            field.queryset = field.queryset.restrict(user, action)
