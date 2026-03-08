# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

CORE_APPS = (
    "core",
    "users",
    "tenancy",
    "ras",
    "account",
)

# ColdFront 1.x legacy apps
LEGACY_APPS = (
    "allocation",
    "project",
    "grant",
    "publication",
    "research_output",
    "resource",
    "field_of_science",
    "user",
)

# Placeholder text for empty tables
EMPTY_TABLE_TEXT = "No results found"

CUSTOMFIELD_EMPTY_VALUES = (None, "", [])

HTML_ALLOWED_TAGS = {
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "dd",
    "del",
    "div",
    "dl",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}


HTML_ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "div": {"class"},
    "h1": {"id"},
    "h2": {"id"},
    "h3": {"id"},
    "h4": {"id"},
    "h5": {"id"},
    "h6": {"id"},
    "img": {"alt", "src", "title"},
    "td": {"align"},
    "th": {"align"},
}

# Boolean widget choices
BOOLEAN_WITH_BLANK_CHOICES = (
    ("", "---------"),
    ("True", "Yes"),
    ("False", "No"),
)
