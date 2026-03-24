![ColdFront](docs/pages/images/logo-lg.png)

# ColdFront - Resource Allocation System

[![Documentation Status](https://readthedocs.org/projects/coldfront/badge/?version=latest)](https://coldfront.readthedocs.io/en/latest/?badge=latest)

ColdFront is an open source resource and allocation management system designed to provide a central portal for administration, reporting, and measuring scientific impact of cyberinfrastructure resources. ColdFront was created to help high performance computing (HPC) centers manage access to a diverse set of resources across large groups of users and provide a rich set of extensible meta data for comprehensive reporting. The flexiblity of ColdFront allows centers to manage and automate their policies and procedures within the framework provided or extend the functionality with [plugins](docs/pages/index.md#extensibility).  ColdFront is written in Python and released under the Apache 2.0 license.

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
