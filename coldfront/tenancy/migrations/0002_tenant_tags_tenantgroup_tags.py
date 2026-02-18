# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_tag_taggeditem"),
        ("tenancy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tenant",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="core.TaggedItem",
                to="core.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="tenantgroup",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="core.TaggedItem",
                to="core.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
