# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_group_managers_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(blank=True, max_length=200, verbose_name="description")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="created")),
                ("expires", models.DateTimeField(blank=True, null=True, verbose_name="expires")),
                ("last_used", models.DateTimeField(blank=True, null=True, verbose_name="last used")),
                (
                    "enabled",
                    models.BooleanField(
                        default=True,
                        help_text="Disable to temporarily revoke this token without deleting it.",
                        verbose_name="enabled",
                    ),
                ),
                (
                    "write_enabled",
                    models.BooleanField(
                        default=True,
                        help_text="Permit create/update/delete operations using this token",
                        verbose_name="write enabled",
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        help_text="v2 token identification key",
                        max_length=12,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(12)],
                        verbose_name="key",
                    ),
                ),
                (
                    "pepper_id",
                    models.PositiveSmallIntegerField(
                        help_text="ID of the cryptographic pepper used to hash the token", verbose_name="pepper ID"
                    ),
                ),
                (
                    "hmac_digest",
                    models.CharField(
                        help_text="SHA256 hash of the token and pepper (v2 only)", max_length=64, verbose_name="digest"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="tokens", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "token",
                "verbose_name_plural": "tokens",
                "ordering": ("-created",),
            },
        ),
    ]
