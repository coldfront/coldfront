# ColdFront - Resource Allocation System

[![Documentation Status](https://readthedocs.org/projects/coldfront/badge/?version=latest)](https://coldfront.readthedocs.io/en/latest/?badge=latest)

ColdFront is an open source resource and allocation management system designed to provide a central portal for administration, reporting, and measuring scientific impact of cyberinfrastructure resources. ColdFront was created to help high performance computing (HPC) centers manage access to a diverse set of resources across large groups of users and provide a rich set of extensible meta data for comprehensive reporting. The flexiblity of ColdFront allows centers to manage and automate their policies and procedures within the framework provided or extend the functionality with [plugins](docs/pages/index.md#extensibility).  ColdFront is written in Python and released under the Apache 2.0 license.

## WARNING UNDER HEAVY DEVELOPMENT

This is the development version of ColdFront currently undergoing heavy development. This is not ready for production use. If you'd like to test out the next version, here's how to get started:

From new database:
```
$ git clone https://github.com/coldfront/coldfront.git
$ cd coldfront
$ git checkout dev/2.0.x
$ uv sync --group docs --group dev --extra initializer
$ DEBUG=True uv run coldfront initial_setup
$ DEBUG=True PLUGINS="coldfront_initializer" uv run coldfront load_test_data
$ DEBUG=True uv run coldfront runserver

# Running the tests:
$ COLDFRONT_ENV=.env.testing uv run -m coverage run -m pytest
```

## Getting Started

* [Official documentation](https://docs.coldfront.dev)
* [Wiki](https://github.com/coldfront/coldfront/wiki)
* [Get Involed](https://coldfront.dev/community/)

## Credits

ColdFront (as of v2.0.0) includes code adopted from [NetBox](https://github.com/netbox-community/netbox). See the NOTICE file. 

## License

ColdFront is released under the Apache 2.0 license. See REUSE.toml.
