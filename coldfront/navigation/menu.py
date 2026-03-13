# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from functools import cache

from django.utils.translation import gettext_lazy as _

from coldfront.registry import registry

from . import Menu, MenuGroup, MenuItem, get_model_item

#
# Nav menus
#

ORGANIZATION_MENU = Menu(
    label=_("Organization"),
    icon_class="fa-solid fa-sitemap",
    groups=(
        MenuGroup(
            label=_("Projects"),
            items=(
                get_model_item("ras", "project", _("Projects")),
                get_model_item("ras", "projectuser", _("Project Users")),
            ),
        ),
        MenuGroup(
            label=_("Tenancy"),
            items=(
                get_model_item("tenancy", "tenant", _("Tenants")),
                get_model_item("tenancy", "tenantgroup", _("Tenant Groups")),
            ),
        ),
    ),
)

ALLOCATIONS_MENU = Menu(
    label=_("Allocations"),
    icon_class="fa-solid fa-list-check",
    groups=(
        MenuGroup(
            label=_("Allocations"),
            items=(
                get_model_item("ras", "allocation", _("Allocations")),
                get_model_item("ras", "allocationtype", _("Allocation Types")),
            ),
        ),
    ),
)

RESOURCES_MENU = Menu(
    label=_("Resources"),
    icon_class="fa-solid fa-server",
    groups=(
        MenuGroup(
            label=_("Resources"),
            items=(
                get_model_item("ras", "resource", _("Resources")),
                get_model_item("ras", "resourcetype", _("Resource Types")),
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
                get_model_item("core", "customfield", _("Custom Fields")),
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
            label=_("Authentication"),
            items=(
                get_model_item("users", "user", _("Users")),
                get_model_item("users", "group", _("Groups")),
                get_model_item("users", "token", _("API Tokens"), staff_only=True),
                get_model_item("users", "objectpermission", _("Permissions"), actions=["add"]),
            ),
        ),
        MenuGroup(
            label=_("System"),
            items=(
                MenuItem(
                    link="core:plugin_list",
                    link_text=_("Plugins"),
                    staff_only=True,
                ),
            ),
        ),
        MenuGroup(
            label=_("Logging"),
            items=(get_model_item("core", "objectchange", _("Change Log"), actions=[]),),
        ),
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
        ALLOCATIONS_MENU,
        RESOURCES_MENU,
        CUSTOMIZATION_MENU,
    ]

    # Add top-level plugin menus
    for menu in registry["plugins"]["menus"]:
        menus.append(menu)

    # Add the default "plugins" menu
    if registry["plugins"]["menu_items"]:
        # Build the default plugins menu
        groups = [MenuGroup(label=label, items=items) for label, items in registry["plugins"]["menu_items"].items()]
        plugins_menu = Menu(label=_("Plugins"), icon_class="fa-solid fa-puzzle-piece", groups=groups)
        menus.append(plugins_menu)

    # Add the admin menu last
    menus.append(ADMIN_MENU)

    return menus
