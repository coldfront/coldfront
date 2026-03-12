-- SPDX-FileCopyrightText: (C) ColdFront Authors
--
-- SPDX-License-Identifier: Apache-2.0

INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0001_initial', CURRENT_TIMESTAMP);
UPDATE django_content_type SET app_label = 'users' WHERE app_label = 'auth' and model = 'user';
