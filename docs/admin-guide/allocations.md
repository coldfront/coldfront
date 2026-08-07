# Allocation Workflow

Allocations grant users access to compute, storage, and other resources.
ColdFront manages allocations through a **finite state machine (FSM) workflow**
powered by [django-viewflow](https://viewflow.org/). Each allocation moves
through a defined set of statuses, with transitions between them controlled
by object-based permissions.

---

## Allocation Lifecycle

### Statuses

An allocation moves through these statuses:

| Status | Description |
|--------|-------------|
| **Requested** | Submitted by a user, awaiting review |
| **Approved** | Approved by a reviewer, ready for activation |
| **Active** | Activated — users have access to the resource |
| **Denied** | Request was denied by a reviewer |
| **Expired** | Reached its `end_date` — access is removed |
| **Revoked** | Revoked by an administrator |
| **Renew** | Submitted for renewal, awaiting approval |

### Status Flow

The workflow defines these transitions:

```
Requested ──approve──→ Approved ──activate──→ Active ──expire──→ Expired
   │  │                    │                     │
   │  └──deny──→ Denied    │                     └──revoke──→ Revoked
   │                       │
   └──renew──→ Renew ──approve──→ Approved
                    └──deny──→ Denied

Active ──renew──→ Renew ──approve──→ Approved ──activate──→ Active
Expired ──renew──→ Renew
Revoked ──renew──→ Renew
Denied ──renew──→ Renew
```

Each transition requires the user to have the corresponding object
permission (e.g., `ras.approve_allocation` to approve). The workflow
also supports **permission callbacks** registered by plugins (see
Transition Callbacks below).

---

## Requesting an Allocation

Users request allocations from a **project detail page** by clicking the
"Request Allocation" button. This opens a form with:

1. **Resource selection** — a dropdown of allocatable resources the user
   can view (filtered by their permissions).
2. **Attribute fields** — custom fields defined by the resource's JSON
   Schema (e.g., number of nodes, GPU hours, storage tier).
3. **Extension fields** — fields from registered allocation extensions
   (see Allocation Extensions below), such as Slurm association settings
   or storage quota limits.
4. **Justification** — a free-text field explaining why the allocation
   is needed.

The form is driven by **HTMX** — selecting a resource dynamically updates
the attribute and extension fields without a full page reload.

On submission, the allocation is created with status `requested` and the
associated extension models (e.g., `SlurmAssociation`, `StorageQuota`) are
created from the form data.

---

## Reviewing Allocations

Reviewers with the `ras.approve_allocation` or `ras.deny_allocation`
permission can act on requested allocations. The review workflow uses
`AllocationReviewForm`, which includes a **comments field**.

### Approving

1. Navigate to the allocation detail page.
2. Click **Approve** — the allocation transitions to `approved`.
3. Optionally add a comment explaining the decision.
4. A notification is sent to the allocation owner.

### Denying

1. Click **Deny** — the allocation transitions to `denied`.
2. Optionally add a comment explaining why it was denied.

Comments added during review are stored as `CommentEntry` records linked
to the allocation. They appear in the allocation's comment thread.

---

## Activating Allocations

Activation moves an allocation from `approved` to `active`. This is the
point where the allocation is considered "live" and users get access to
the resource.

The `AllocationActivateForm` allows the reviewer to set:

- **Start date** and **end date**
- **Resource attribute values** (pre-filled from the request)
- **Extension field values** (pre-filled from the request)

On activation, the allocation's extension models are **created or updated**
from the form data. For example, `SlurmAssociation` records are created
for the allocation's Slurm account, partition, and user association data.

Plugins can register **target callbacks** for the `active` state to
provision access on external systems (see Target Callbacks below).

---

## Renewing Allocations

Renewal allows an allocation to continue past its current term. The
renewal flow:

1. An allocation in `active`, `expired`, `revoked`, or `denied` status
   can be submitted for renewal.
2. On submission, the allocation enters `renew` status.
3. A reviewer approves or denies the renewal request.
4. If approved, the allocation moves to `approved` and can be activated
   again (typically with a new `end_date`).

---

## Expiration and Revocation

- **Expiration** happens automatically when an allocation's `end_date` is
   reached. The workflow transitions the allocation to `expired`. Plugins
   can register callbacks for this state to deprovision access.
- **Revocation** is an admin action that immediately terminates an active
   allocation, moving it to `revoked`.

---

## Allocation Extensions

Extensions add resource-specific data to allocations. They are registered
via `register_allocation_extension()` and implemented as Django models
with a unique FK back to the allocation.

### Built-in Extensions

| Extension | Resource Type | Purpose |
|-----------|---------------|---------|
| `SlurmAssociation` | `slurm.SlurmCluster`, `slurm.SlurmPartition` | Links allocation to Slurm accounting (account, partition, fairshare, job limits) |
| `StorageQuota` | `storage.StorageResource` | Links allocation to storage quotas (hard/soft limits, file counts) |

### Requestable Fields

Each extension model defines `requestable_fields()` — a list of field
names that should appear on the allocation request form and the change
request form. These fields are dynamically added by
`AllocationExtensionFormMixin`.

For example, `SlurmAssociation` defines:

```python
_requestable_fields = [
    "fairshare",
    "max_jobs",
    "max_submit_jobs",
    "max_wall_duration_per_job",
]
```

These fields appear as a "Slurm Association Details" section on the
allocation request form. At activation time, the values are used to
create the extension instance.

Extensions can also define `requestable_fields_overrides()` to replace
auto-generated form fields with custom widgets or validation.

### Creating Custom Extensions

To add a new extension type:

1. Create a model inheriting from `AllocationExtensionMixin`.
2. Set `_requestable_fields` to the list of fields exposed in forms.
3. Register the extension with `@register_allocation_extension(ResourceModel)`.
4. Override `create_for_allocation()` for custom creation logic.
5. Override `apply_json_change()` for custom change request application.

The extension appears automatically on allocation request forms, activation
forms, and change request forms for the registered resource type.

---

## Allocation Change Requests

Change requests allow PIs and project owners to propose modifications to
**active** allocations without going through the full allocation workflow.

### Change Request Lifecycle

Change requests have their own status flow:

```
Requested ──approve──→ Approved ──apply──→ Applied
   │
   └──deny──→ Denied
```

| Status | Description |
|--------|-------------|
| **Requested** | Submitted by a user, awaiting review |
| **Approved** | Approved by a reviewer, ready to apply |
| **Denied** | Request was denied |
| **Applied** | Changes have been applied to the allocation |

### Creating a Change Request

From the allocation detail page, users with the
`ras.add_allocationchangerequest` permission see a "Request Change" button.
The change request form dynamically shows:

1. **Extension (days)** — a dropdown of predefined durations (7, 30, 90,
   365 days) to extend the allocation's `end_date`.
2. **Attribute changes** — resource schema fields pre-filled with current
   values. Only fields the user changes are included in the request.
3. **Extension changes** — requestable fields from registered extensions
   (e.g., fairshare, max_jobs for Slurm associations), pre-filled with
   current values.

At least one change must be proposed (extension, attributes, or extension
changes). A justification field explains why the change is needed.

### Reviewing Change Requests

Reviewers with `ras.approve_allocationchangerequest` or
`ras.deny_allocationchangerequest` permission can approve or deny change
requests. Like allocation reviews, the review form includes a **comments
field** that creates a `CommentEntry` on the change request.

### Applying Changes

When a reviewer clicks **Apply**, the system atomically:

1. Snapshots the allocation's current `attribute_data` and extension field
   values (stored on the change request for audit).
2. Applies `extension_days` — adds the specified days to the allocation's
   `end_date`.
3. Applies `attribute_changes` — merges the proposed keys into the
   allocation's `attribute_data` and **validates** the result against the
   resource's JSON Schema.
4. Applies `extension_changes` — calls `apply_json_change()` on each
   extension model, which validates and saves the proposed field values.
5. Saves the allocation and all modified extension models.
6. Sets the change request status to `applied`.

**Once applied, the change request becomes read-only.** The edit view
disables all form fields for applied requests, and POST requests are
blocked with a `PermissionDenied` exception.

### Viewing the Diff

The change request detail page shows a side-by-side comparison:

- **Current values** (left) vs. **Requested changes** (right) for
  unapplied requests.
- **Original values** (left) vs. **Applied values** (right) for applied
  requests (using the stored snapshots).

Differences are highlighted — added/changed values in green, removed
values in red.

---

## Transition Callbacks

ColdFront workflows support two types of plugin hooks: **target callbacks**
and **permission callbacks**.

### Target Callbacks

Target callbacks fire **after** a transition successfully reaches a target
state. They are used for side-effects like provisioning external systems,
sending notifications, or updating related records.

The Slurm and Storage apps register callbacks for allocation activation
and expiration to create and remove Slurm associations and storage quotas.

Register a target callback:

```python
from coldfront.registry import register_target_callback
from coldfront.ras.flows.allocations import AllocationStatusFlow
from coldfront.ras.choices import AllocationStatusChoices


@register_target_callback(
    AllocationStatusFlow,
    AllocationStatusChoices.STATUS_ACTIVE,
)
def on_allocation_activated(allocation, *, source, target):
    """
    Called when an allocation transitions to 'active'.
    Provisions the allocation on the external resource.
    """
    resource = allocation.resource_object
    if hasattr(resource, "provision_allocation"):
        resource.provision_allocation(allocation)
```

The callback receives `(obj, *, source, target)` where `obj` is the
allocation instance. Callbacks are wrapped in try-except — if one fails,
other callbacks still run and an admin notification is sent.

Available target states for `AllocationStatusFlow`:

| State constant | Value | Typical use |
|----------------|-------|-------------|
| `STATUS_REQUESTED` | `"requested"` | Logging, notification |
| `STATUS_APPROVED` | `"approved"` | Pre-activation checks |
| `STATUS_ACTIVE` | `"active"` | Provision resource access |
| `STATUS_DENIED` | `"denied"` | Cleanup |
| `STATUS_EXPIRED` | `"expired"` | Deprovision resource access |
| `STATUS_REVOKED` | `"revoked"` | Deprovision resource access |
| `STATUS_RENEW` | `"renew"` | Renewal notification |

For change requests (`AllocationChangeRequestFlow`):

| State constant | Value | Typical use |
|----------------|-------|-------------|
| `STATUS_REQUESTED` | `"requested"` | Notify reviewers |
| `STATUS_APPROVED` | `"approved"` | Pre-apply validation |
| `STATUS_DENIED` | `"denied"` | Notify requester |
| `STATUS_APPLIED` | `"applied"` | Post-apply notification |

### Permission Callbacks

Permission callbacks run **before** a transition is allowed. They can block
a transition based on custom logic — for example, ensuring an allocation
can only be activated during business hours, or that a user has completed
required training.

Register a permission callback:

```python
from coldfront.registry import register_transition_permission_callback
from coldfront.ras.flows.allocations import AllocationStatusFlow


@register_transition_permission_callback(
    AllocationStatusFlow,
    "activate",
)
def on_activate_check(allocation, user):
    """
    Only allow activation if the allocation's resource is online.
    """
    resource = allocation.resource_object
    return resource is not None and resource.status == "active"
```

The callback receives `(obj, user)` and must return `True` (allow) or
`False` (deny). If **any** registered permission callback returns `False`,
the transition is blocked — all callbacks must pass.

Available transition slugs for `AllocationStatusFlow`:

| Transition slug | Default permission | Source states |
|----------------|-------------------|---------------|
| `request` | `ras.request_allocation` | `requested` (self-loop for creation) |
| `approve` | `ras.approve_allocation` | `requested`, `renew` |
| `deny` | `ras.deny_allocation` | `requested`, `renew` |
| `activate` | `ras.activate_allocation` | `approved` |
| `expire` | `ras.expire_allocation` | `active` |
| `renew` | `ras.renew_allocation` | `active`, `expired`, `revoked`, `denied` |
| `revoke` | `ras.revoke_allocation` | `active` |

For change requests (`AllocationChangeRequestFlow`):

| Transition slug | Default permission | Source states |
|----------------|-------------------|---------------|
| `approve` | `ras.approve_allocationchangerequest` | `requested` |
| `deny` | `ras.deny_allocationchangerequest` | `requested` |
| `apply` | `ras.apply_allocationchangerequest` | `approved` |

---

## How Callbacks Work

The `ColdFrontFlow` base class maintains two registries:

- **`_target_callbacks`** — a dict mapping target state values to lists of
  callback functions.
- **`_transition_permission_callbacks`** — a dict mapping transition slugs
  to lists of callback functions.

Each subclass gets its own registries (via `__init_subclass__`), so
callbacks registered for `AllocationStatusFlow` do not affect
`AllocationChangeRequestFlow`.

The `_dispatch_target_callbacks()` method iterates over all callbacks for
the target state. If a callback raises an exception, it is logged and a
system notification is sent to administrators — the core state transition
is **not** rolled back.

The `_check_permission_callbacks()` method iterates over permission
callbacks for the transition slug. If any returns `False`, the transition
is denied with the standard "permission denied" response.

### Callback Registration API

```python
# Decorator form (recommended)
from coldfront.registry import register_target_callback
from coldfront.registry import register_transition_permission_callback


@register_target_callback(AllocationStatusFlow, "active")
def my_callback(allocation, *, source, target): ...


@register_transition_permission_callback(AllocationStatusFlow, "activate")
def my_permission_check(allocation, user): ...


# Direct method form (equivalent)
AllocationStatusFlow.register_target_callback("active", my_callback)
AllocationStatusFlow.register_transition_permission_callback(
    "activate",
    my_permission_check,
)
```

---

## Notifications

ColdFront sends notifications when allocations are approved. The
`AllocationStatusFlow._on_success_transition()` method checks for the
`approved` target state and sends a notification to the allocation owner
via the `AllocationsNotificationType` notification system.

Notifications use the `generic_notifications` framework and appear in
the user's notification inbox. Plugins can send additional notifications
by registering target callbacks for other states.

---

## Permissions Summary

| Action | Permission codename | Default scope |
|--------|---------------------|---------------|
| View allocation | `ras.view_allocation` | Default: own + team |
| Request allocation | `ras.request_allocation` | Default: own project |
| Approve allocation | `ras.approve_allocation` | Admin-assigned |
| Deny allocation | `ras.deny_allocation` | Admin-assigned |
| Activate allocation | `ras.activate_allocation` | Admin-assigned |
| Renew allocation | `ras.renew_allocation` | Admin-assigned |
| Revoke allocation | `ras.revoke_allocation` | Admin-assigned |
| Expire allocation | `ras.expire_allocation` | System (auto) |
| View change request | `ras.view_allocationchangerequest` | Default: own allocation |
| Add change request | `ras.add_allocationchangerequest` | Default: own allocation |
| Approve change request | `ras.approve_allocationchangerequest` | Admin-assigned |
| Deny change request | `ras.deny_allocationchangerequest` | Admin-assigned |
| Apply change request | `ras.apply_allocationchangerequest` | Admin-assigned |

All permissions use ColdFront's object-based permission system with JSON
constraints, allowing HPC centers to define granular access rules (e.g.,
"only approve allocations in the Physics tenant").
