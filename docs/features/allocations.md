# Allocation Workflow

Allocations grant users access to resources. ColdFront uses a status
workflow to manage allocations from request through approval, activation,
renewal, and expiration. The workflow is powered by
[django-viewflow](https://viewflow.org/) using finite state machine (FSM)
transitions.

## Statuses

An allocation moves through these statuses:

| Status | Description |
|---|---|
| **Requested** | The allocation has been submitted and is awaiting review |
| **Approved** | The allocation has been approved and is ready for activation |
| **Active** | The allocation is active and users have access to the resource |
| **Denied** | The allocation request was denied |
| **Expired** | The allocation reached its end date |
| **Revoked** | The allocation was revoked by an administrator |
| **Renewed** | The allocation was renewed for a new term |

## Transitions

The workflow defines these transitions between statuses:

```
Requested → Approved → Active → Expired
   ↓          ↓           ↓
 Denied     Denied      Revoked

Active → Renewed → [back to workflow]
```

Each transition requires a permission check. Only users with the
appropriate permission can perform a transition.

## Allocation Extensions

Allocations support extensions through the `AllocationExtensionMixin`.
Extensions let you add custom behavior to allocations. For example, the Slurm
app registers a `SlurmAssociation` extension that links allocations to Slurm
accounting. Extensions are registered using `register_allocation_extension`.
Each allocation extension can define a list of `requestable fields` that define
which fields on the object are added to the allocation request form.

## Allocation Change Requests

Allocation change requests let users request modifications to an active
allocation. The change request workflow has its own status flow:

```
Requested → Approved → Activated
  ↓
Denied
```

Change requests can modify allocation attributes such as the end date or
custom schema fields. When approved, the changes can be applied to the
allocation by an admin.

## Transition Permissions

Each transition in the allocation workflow has a permission check. You can
configure who can perform each transition by assigning object permissions.
The workflow checks the permission for the model and action before allowing
a transition.

## Target Callbacks

When an allocation transitions to a target status, the workflow dispatches
target callbacks. Plugins can register callbacks for specific status
transitions using `register_target_callback`. For example, the Slurm and
Storage apps register callbacks that fire when an allocation is activated
or expired.

To register a callback:

```python
from coldfront.ras.flows.allocations import AllocationStatusFlow
from coldfront.registry import register_target_callback


@register_target_callback(AllocationStatusFlow, "active")
def on_allocation_activated(allocation, *, source, target):
    # Run code when an allocation has been activated
    pass
```

## Custom Allocation Attributes

Resources with a `schema` JSON field define custom attributes that are captured
per allocation. The schema uses JSON Schema format and supports types such as
text, integer, boolean, and select. These fields appear on the allocation
request form and the values are stored in the allocation's `attribute_data`
field.
