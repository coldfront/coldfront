# Storage

ColdFront has a Storage app (`coldfront.storage`) that manages allocations to
storage resources. Storage allocations carry a quota amount and the lifecycle
creates and removes paths and quotas on the storage system.

## Storage Resources

A **StorageResource** is an allocatable storage resource. Users request an
allocation to a storage resource and specify the requested quota amount on
a separate form. Each storage resource is backed by one or more storage
clusters.

## Storage Clusters

A **StorageCluster** represents a storage system backend. It has a
`backend_path` field that points to a Python class implementing the
`StorageBackend` interface. The cluster stores no connection settings —
each backend handles its own configuration.

## Storage Quotas

A **StorageQuota** bridges an allocation to a storage resource. It carries
the path, ownership, and quota limits such as:

- **hard_limit** — The approved quota limit in bytes
- **hard_limit_requested** — The user's requested amount
- **soft_limit** — A warning threshold before the hard limit
- **hard_limit_files** and **soft_limit_files** — File count limits
- **share_type** — POSIX, SMB, or NFS share type

The path is auto-generated from a template on the storage resource. The
template supports variables such as `{project.slug}` and `{allocation.id}`.
Admins can override the path before activation.

## Backend Plugin System

Each storage backend is a Python class that implements the abstract
`StorageBackend` interface. The interface defines methods for creating
paths, creating quotas, updating quotas, and removing quotas. Backends
are auto-discovered at startup and can also be registered by plugins.

## Snapshot Policies

Storage clusters can define snapshot policies with an interval, retention
days, and extra configuration. Each quota can optionally select a snapshot
policy. The backend receives the policy details when creating or removing
the snapshot schedule.

## Sync Mechanism

The storage integration uses the same hybrid approach as Slurm:

1. **Targeted handlers** — When an allocation is activated, the system
   creates the path and quota on each cluster. When an allocation expires
   or is revoked, the system removes the quota and optionally locks the
   path.

2. **Periodic batch sync** — A scheduled job runs full reconciliation of
   storage quotas against the backend state.

## Capacity Tracking

Both storage resources and clusters track capacity, allocated, and used
bytes. Callbacks update allocated bytes atomically on activation and
expiration. The sync engine updates used bytes from the backend.
