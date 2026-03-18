# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand

from coldfront.utils.migrator import migrate_all


class Command(BaseCommand):
    help = "Upgrade the Coldfront database to version 2.0"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f", "--force_overwrite", help="Force upgrade to run with no warning.", action="store_true"
        )

    def handle(self, *args, **options):
        if options["force_overwrite"]:
            self.run_updater()

        else:
            self.stdout.write(
                self.style.WARNING(
                    """WARNING: Running this command upgrades the ColdFront database to version 2.0 and may modify/delete data in your existing ColdFront database. Run with caution!"""
                )
            )
            user_response = input("Do you want to proceed?(yes):")

            if user_response == "yes":
                self.run_updater()
            else:
                self.stdout.write("Please enter 'yes' if you wish to run the updater.")

    def run_updater(self):
        migrate_all()
