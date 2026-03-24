# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.core.management import call_command
from django.core.management.base import BaseCommand

ALLOWED_APPS = [
    "core",
    "contenttypes",
    "auth",
    "users",
    "account",
    "admin",
    "ras",
    "tenancy",
    "sessions",
]


class Command(BaseCommand):
    help = "Initial setup of the Coldfront database"

    def handle(self, *args, **options):
        for app in ALLOWED_APPS:
            call_command("migrate", app)
