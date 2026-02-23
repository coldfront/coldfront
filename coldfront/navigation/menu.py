# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from functools import cache

from django.utils.translation import gettext_lazy as _

from . import Menu, MenuGroup, get_model_item

#
# Nav menus
#

ORGANIZATION_MENU = Menu(
    label=_("Organization"),
    icon_class="fa-solid fa-sitemap",
    groups=(
        MenuGroup(
            label=_("Tenancy"),
            items=(
                get_model_item("tenancy", "tenant", _("Tenants")),
                get_model_item("tenancy", "tenantgroup", _("Tenant Groups")),
            ),
        ),
    ),
)

CUSTOMIZATION_MENU = Menu(
    label=_("Customization"),
    icon_class="fa-solid fa-sliders",
    groups=(
        MenuGroup(
            label=_("Customization"),
            items=(
                get_model_item("core", "customfieldchoiceset", _("Custom Field Choices")),
                get_model_item("core", "tag", "Tags"),
            ),
        ),
    ),
)

ADMIN_MENU = Menu(
    label=_("Admin"),
    icon_class="fa-solid fa-screwdriver-wrench",
    groups=(
        MenuGroup(
            label=_("Logging"),
            items=(get_model_item("core", "objectchange", _("Change Log"), actions=[]),),
        ),
        #        MenuGroup(
        #            label=_("Authentication"),
        #            items=(
        #                get_model_item("users", "user", _("Users")),
        #                get_model_item("users", "group", _("Groups")),
        #            ),
        #        ),
    ),
)


@cache
def get_menus():
    """
    Dynamically build and return the list of navigation menus.
    This ensures plugin menus registered during app initialization are included.
    The result is cached since menus don't change without a Django restart.
    """
    menus = [
        ORGANIZATION_MENU,
        CUSTOMIZATION_MENU,
    ]

    # Add top-level plugin menus
    # for menu in registry["plugins"]["menus"]:
    #    menus.append(menu)

    # Add the default "plugins" menu
    # if registry["plugins"]["menu_items"]:
    #    # Build the default plugins menu
    #    groups = [MenuGroup(label=label, items=items) for label, items in registry["plugins"]["menu_items"].items()]
    #    plugins_menu = Menu(label=_("Plugins"), icon_class="fa-solid fa-puzzle-piece", groups=groups)
    #    menus.append(plugins_menu)

    # Add the admin menu last
    menus.append(ADMIN_MENU)

    return menus
