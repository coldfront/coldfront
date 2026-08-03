---
icon: lucide/arrow-up
---

# Upgrading ColdFront

This document describes how to upgrade ColdFront. New releases of ColdFront
can introduce breaking changes. Refer to this document before you upgrade.

## Upgrade from v1 to v2

ColdFront v2.0.0 is a complete rewrite. The upgrade from v1 to v2 is a
significant change and is currently a work in progress.

!!! warning "Pre-production software"

    ColdFront v2.0.0 is under heavy development and is not ready for
    production use. The upgrade path from v1 to v2 is not complete.

### Database changes

v2 uses a new user model. If you have an existing v1 database, you must
convert the user model before you run the database migrations.

To upgrade an existing v1 database:

```
$ git clone https://github.com/coldfront/coldfront.git
$ cd coldfront
$ uv sync
$ uv run coldfront dbshell < scripts/upgrade-v2.0.0-user-model.sql
$ uv run coldfront migrate
$ uv run coldfront upgrade_v2
```

### Known limitations

- The upgrade script is a work in progress. Some data from v1 may not
  transfer to v2 correctly.
- v2 uses a different data model. Some features from v1 are not yet
  available in v2.
- Custom plugins from v1 must be rewritten for v2.

## Upgrade within v2

Upgrade instructions for minor releases within v2 are not yet available.
This section will be updated as v2 approaches production readiness.
