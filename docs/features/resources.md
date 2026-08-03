# Generic Resources

Generic resources are assets that can be allocated to users. Each resource
has a name, a status, and an optional resource type. Resources can be
organized in a hierarchy using parent-child relationships.

## Resource Types

A Resource Type categorizes resources. For example, you can create types
such as "Cluster", "Partition", or "Storage". Each resource type has a
name and a color for display in the user interface.

## Resource Hierarchy

Resources use MPTT (Modified Preorder Tree Traversal) to support
hierarchical relationships. A resource can have a parent resource. This
lets you model nested structures such as a cluster containing partitions for example.

## Tags and Custom Fields

Resources support tags, custom fields, and custom attributes for organization
and filtering. See [Customization](customization.md) for details.

## Tenancy

Resources can be assigned to a Tenant for multi-tenant organization. See
[Tenancy](tenancy.md) for details.
