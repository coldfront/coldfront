# Tenancy

ColdFront supports multi-tenant organization.

## Tenants

A Tenant represents an organization, school, department, or other group.
Tenants can be assigned to resources, projects, and allocations. This
lets you track which parts of your infrastructure belong to which
organization.

## Tenant Groups

Tenants can be organized into Tenant Groups. A Tenant Group is an
arbitrary collection of tenants. Groups use MPTT to support hierarchical
relationships, so you can nest groups within groups.

## Using Tenancy

Tenants can be assigned to:

- **Resources** — Track which organization owns a resource
- **Projects** — Associate a project with an organization
- **Allocations** — Associate an allocation with an organization

In the user interface, tenant information appears in list views and detail
views. List views can be filtered by tenant. Forms include tenant fields
when creating or editing objects.
