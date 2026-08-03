# Projects

A Project is a container that organizes research summary information and
holds allocations. Projects are the main organizational unit in ColdFront.
Each project has an owner, a name, and can be associated with a Group.

## Project Users

Projects can have multiple users. Each user is a member of the project
through a `ProjectUser` record. The project owner can add or remove users.

When you add a user to a project, they can request allocations under that
project and be included in active allocations.

## Groups

A Project can be associated with a Group. The Group is a model from
`coldfront.users.models.Group`, not Django's built-in group. When a user
is added to a project, they are automatically added to the project's
Group. This helps manage access at the group level.

## Allocations

Projects are the parent of allocations. Each allocation belongs to one
project. The project's users are the users that can be included in the
allocation. There is no separate `AllocationUser` model in ColdFront —
allocation users come directly from the project's `ProjectUser` records.

## Tenancy

Projects can be assigned to a Tenant for multi-tenant organization. See
[Tenancy](tenancy.md) for details.
