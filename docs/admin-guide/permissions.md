# Object-Based Permissions

ColdFront uses a **object-based permission system** that allows administrators to define granular permissions scoped to specific records, fields, and relationships. Unlike Django's all-or-nothing model permissions, ColdFront can restrict access to individual records based on their attributes.

---

## Core Concepts

### Actions

Permissions map to Django-style codenames: `{app_label}.{action}_{model}`. Four built-in CRUD actions plus custom workflow actions.

| Action | Description |
|--------|-------------|
| `view` | Read/view an object |
| `add` | Create a new object |
| `change` | Edit/update an existing object |
| `delete` | Delete an object |

Custom actions are registered via `Meta.permissions`. Allocation workflow actions:

| Action | Codename | Description |
|--------|----------|-------------|
| `request` | `ras.request_allocation` | Request a new allocation |
| `approve` | `ras.approve_allocation` | Approve pending allocation |
| `deny` | `ras.deny_allocation` | Deny pending allocation |
| `activate` | `ras.activate_allocation` | Activate approved allocation |
| `renew` | `ras.renew_allocation` | Renew active allocation |
| `revoke` | `ras.revoke_allocation` | Revoke an allocation |
| `expire` | `ras.expire_allocation` | Expire an allocation |

### Object Types & Constraints

Each ObjectPermission targets one or more ContentTypes (models). **Constraints** are JSON queryset filters that restrict *which records* the user can act on. They support:

- Django ORM field lookups (`field__lookup: value`)
- `$user` token — replaced with the current user's PK at runtime
- `$queryset` expression — dynamic subquery against another model

Multiple keys in one JSON object are **AND'd**. Multiple objects in the array are **OR'd**. A `null` entry grants unrestricted access.

### Roles

Roles bundle ObjectPermissions into reusable profiles (e.g., "Principal Investigator") that can be assigned to users and groups.

---

## Default Permissions

Configured via `DEFAULT_PERMISSIONS` in settings. Every authenticated user gets:

- Manage their own API tokens
- View unlocked resources (Generic Resources, Slurm clusters/partitions, Storage Resources)
- View projects they own or belong to
- View project users for associated projects
- View allocations they own or are members of
- View Slurm associations and Storage quotas for their allocations

---

## Constraint Reference

> **JSON escaping:** A backslash (`\`) is a JSON escape character. A regex containing `\.` must be entered as `\\.`.

| Pattern | Constraint JSON | Description |
|---------|----------------|-------------|
| Exact match | `{"status": "active"}` | Field equals value |
| Multi-value | `{"status__in": ["active", "pending"]}` | Field is one of several values |
| AND | `{"status": "active", "role": "testing"}` | Multiple fields must all match |
| Negation | `{"locked": false}` | Field is false |
| Prefix (case) | `{"name__startswith": "hpc-"}` | Name starts with string |
| Suffix (case-insensitive) | `{"name__iendswith": ".example.edu"}` | Name ends with string |
| Regex | `{"name__regex": "^hpc-[0-9]+$"}` | Name matches regex |
| Numeric range | `{"vid__gte": 100, "vid__lt": 200}` | Range filter (AND) |
| OR | `[{"vid__lt": 200}, {"status": "reserved"}]` | Either condition matches |
| User token | `{"owner": "$user"}` | Self-referential — current user |
| User token (OR) | `[{"project__owner": "$user"}, {"project__users__user": "$user"}]` | User owns or is member |
| Unrestricted | `null` | All records accessible |

### Relationship Traversal

Constraints traverse FK and M2M relationships using Django's `__` syntax.

| Traversal | Constraint | Meaning |
|-----------|------------|---------|
| Forward FK | `{"project__owner": "$user"}` | Project's owner is user |
| Reverse FK | `{"project__users__user": "$user"}` | User is a project member |
| Multi-hop | `{"allocation__project__tenant__name": "Physics"}` | Allocation's project's tenant is Physics |

---

## The `$user` Token

Replaced at runtime with the current user's PK. Enables self-referential constraints.

| Use | Constraint |
|-----|------------|
| Own record | `{"owner": "$user"}` |
| Owns related project | `{"project__owner": "$user"}` |
| Is project member | `{"project__users__user": "$user"}` |
| Created the record | `{"created_by": "$user"}` |

**Limitation:** The token resolves to the user's **PK**, not a username or other field. `{"owner__username": "$user"}` would compare a PK against username strings and never match.

---

## The `$queryset` Expression

Enables dynamic subqueries for GenericForeignKey traversal and cross-model filtering where simple field lookups can't express the filter.

### Syntax

```json
[
    {
        "{field}__in": {
            "$queryset": {
                "model": "{app_label}.{model_name}",
                "filter": {
                    "{field_lookup}": "{value}"
                }
            }
        }
    }
]
```

At runtime: resolves `model` via `apps.get_model()`, builds a queryset from `filter`, extracts PKs, and uses them in the `__in` lookup — generating a SQL subquery.

### Common Use Cases

| Use case | Constraint | What it does |
|----------|------------|-------------|
| GFK traversal | `{"resource_object_id__in": {"$queryset": {"model": "ras.allocation", "filter": {"project__owner": "$user"}}}, "resource_object_type__model": "allocation"}` | Filter GFK records by target model attributes |
| Group membership | `{"assigned_group_id__in": {"$queryset": {"model": "users.group", "filter": {"users": "$user"}}}}` | Records assigned to user's groups |
| Tenant scope | `{"tenant_id__in": {"$queryset": {"model": "tenancy.tenant", "filter": {"groups__users": "$user"}}}}` | Resources in user's tenant |
| Aggregate filter | `{"id__in": {"$queryset": {"model": "ras.project", "filter": {"allocations__status__in": ["requested", "renew"]}}}}` | Projects with allocations in specific status |

---

## Permissions Enforcement

### Viewing Objects

When a request arrives, ColdFront checks if the user has the required permission (e.g., `ras.view_allocation`). If granted, any constraints are compiled into Django Q filters and applied to the database query. Multiple ObjectPermissions for the same action are OR'd. For example, a user with both `{"owner": "$user"}` and `{"project__users__user": "$user"}` constraints on `ras.view_allocation` gets:

```python
Allocation.objects.filter(Q(owner=request.user) | Q(project__users__user=request.user))
```

### Creating and Modifying Objects

ColdFront validates the change inside an atomic transaction: the object is created/saved, then a second query retrieves it through the restricted queryset using its PK. If the query fails (the new revision doesn't match the constraint), the transaction rolls back and the user is notified. This is why constraints on add/change permissions work — the object exists at constraint-check time even though it didn't at permission-check time.

---

## Adding Custom Permissions

Via the admin UI: **Users → Object Permissions** → **Add Object Permission**. Set a name, select object types, choose actions, define constraints, and assign to users/groups. Roles are managed at **Users → Roles**.

---

## Permission Naming Convention

ObjectPermissions need unique names. Use this convention to keep the catalog readable when creating multiple permissions for the same model with different constraints.

### Format

```
{access}/{scope}/{model}[/{constraint_detail}]
```

### Access Levels

| Token | Meaning |
|-------|---------|
| `read` | View-only (`view` action) |
| `write` | Full CRUD (`view`, `change`, `add`, `delete`) |
| `read:{qualifier}` | View + hinted custom actions |
| `write:{qualifier}` | View + hinted custom actions (qualifier replaces standard CRUD) |

The qualifier hints at included actions (e.g., `request`, `review`, `renew`, `edit`, `add`). Multiple actions use colons: `write:request:renew`.

### Scopes

| Token | Constraint pattern |
|-------|--------------------|
| `all` | None (unrestricted) |
| `self` | `{"owner": "$user"}` — own records only |
| `team` | `[{"owner": "$user"}, {"users__user": "$user"}]` — owner or member |
| `tenant:{name}` | `{"tenant__name": "{name}"}` — tenant-scoped |

### Constraint Detail (Optional)

Appended after the model when scope alone isn't enough: `/unlocked`, `/active`, `/allocation`.

### Examples

| Name | Actions | Constraints |
|------|---------|-------------|
| `write/self/project` | view, add, change, delete | `{"owner": "$user"}` |
| `read/self/allocation` | view | `{"project__owner": "$user"}` |
| `write:request:renew/self/allocation` | view, request, renew | `{"project__owner": "$user"}` |
| `write:add/self/allocationchangerequest` | view, add | `{"allocation__project__owner": "$user"}` |
| `write/team/projectuser` | view, add, change, delete | `[{"project__owner": "$user"}, {"project__users__user": "$user"}]` |
| `read/all/user` | view | none |
| `read/all/projectuser` | view | none |
| `write:review/all/allocation` | view, approve, deny | none |
| `read/all/project` | view | none |
| `read/all/commententry` | view | none |
| `write:add/all/commententry` | view, add | none |
| `write:add/self/commententry/allocation` | view, add | GFK constrained to allocation comments |
| `write:edit/self/commententry` | view, change, delete | `{"created_by": "$user"}` |
| `read/tenant:physics/project` | view | `{"tenant__name": "Physics"}` |
| `write:review/tenant:physics/allocation` | view, approve, deny | `{"project__tenant__name": "Physics"}` |

---

## Key Points

- **Default permissions** ensure basic functionality — users see their own projects, allocations, and resources
- **Constraints** are Django ORM Q filters — any valid field lookup works
- **`$user`** resolves to the current user's PK at runtime
- **`$queryset`** enables dynamic subqueries for GFK and cross-model filtering
- **Roles** bundle permissions into reusable profiles
- **Permissions are additive** — union of direct, group, and role assignments
- **Superusers** (`is_superuser=True`) bypass all permission checks
