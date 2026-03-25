![ColdFront](docs/pages/images/logo-lg.png)

# ColdFront - Resource Allocation System

[![Documentation Status](https://readthedocs.org/projects/coldfront/badge/?version=latest)](https://coldfront.readthedocs.io/en/latest/?badge=latest)

ColdFront is an open source resource and allocation management system designed to provide a central portal for administration, reporting, and measuring scientific impact of cyberinfrastructure resources. ColdFront was created to help high performance computing (HPC) centers manage access to a diverse set of resources across large groups of users and provide a rich set of extensible meta data for comprehensive reporting. The flexiblity of ColdFront allows centers to manage and automate their policies and procedures within the framework provided or extend the functionality with [plugins](docs/pages/index.md#extensibility).  ColdFront is written in Python and released under the Apache 2.0 license.

## WARNING UNDER HEAVY DEVELOPMENT

This is the development version of ColdFront currently undergoing heavy development. This is not ready for production use. If you'd like to test out the next version, here's how to get started:

From new database:
```
$ git clone https://github.com/coldfront/coldfront.git
$ cd coldfront
$ git checkout feature/v2-poc
$ uv sync --group docs --group dev --extra initializer
$ DEBUG=True uv run coldfront initial_setup
$ DEBUG=True PLUGINS="coldfront_initializer" uv run coldfront load_test_data
$ DEBUG=True uv run coldfront runserver

# Running the tests:
$ COLDFRONT_ENV=.env.testing uv run -m coverage run -m pytest
```

From existing database (note: proceed with extreme caution):
```
$ git clone https://github.com/coldfront/coldfront.git
$ cd coldfront
$ git checkout feature/v2-poc
$ uv sync --group docs --group dev
$ uv run coldfront dbshell < scripts/upgrade-v2.0.0-user-model.sql
$ uv run coldfront migrate
$ uv run coldfront upgrade_v2
```
How to write a plugin: [see example](https://github.com/coldfront/coldfront-project-review)

```
$ uv init --lib coldfront-my-plugin
$ cd coldfront-my-plugin
$ edit src/coldfront_my_plugin/__init__.py

from coldfront.plugins import PluginConfig

from .version import __version__


class ColdFrontMyPluginConfig(PluginConfig):
    name = "coldfront_my_plugin"
    verbose_name = "ColdFront My Plugin"
    version = __version__
    description = "Add your description here"
    author = "My Name"
    author_email = "my email"
    base_url = "my_plugin"
    min_version = "2.0.0"
    default_settings = {}

config = ColdFrontMyPluginConfig
```

## Features

- Allocation based system for managing access to resources
- Self-service portal for users to request access to resources for their research group
- Ability to define custom attributes on resources and allocations 
- Integration with 3rd party systems for automation, access control, and other system provisioning tasks

## Getting Started

* [Official documentation](https://docs.coldfront.dev)
* [Wiki](https://github.com/coldfront/coldfront/wiki)

## Credits

ColdFront (as of v2.0.0) is a derivative of [NetBox](https://github.com/netbox-community/netbox) and would not exist without their excellent open source code base to start from. We specifically adopted NetBox's underlying data model, generic views, plugin system, tagging, custom fields, and object based permission system and ported it for use with ColdFront's resource allocation system.

## License

ColdFront is released under the Apache 2.0 license. See REUSE.toml.
