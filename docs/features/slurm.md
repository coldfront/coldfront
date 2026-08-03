# Slurm

ColdFront has a Slurm app (`coldfront.slurm`) that integrates with
[Slurm](https://slurm.schedmd.com/) workload manager accounting. The
integration maps ColdFront allocations to Slurm accounting entities and
synchronizes them using the Slurm REST API.

## Slurm Entities

ColdFront models the following Slurm entities:

- **SlurmCluster** — A compute cluster managed by Slurm. Has a name,
  tenant, default QOS, fairshare, features, and classification.
- **SlurmPartition** — A named partition within a cluster. Has limits
  such as max jobs, max TRES per job, and wall duration. Each partition
  has an `allow_qos` list and a single assigned QOS.
- **SlurmQOS** — A Quality of Service profile. Defines priority, job
  limits per user and account, and wall duration limits.
- **SlurmAccount** — A named Slurm accounting account. Accounts are lean
  containers with a name, description, and organization. All per-association
  limits live on the association instead.
- **SlurmAssociation** — Bridges an Allocation to its SlurmAccount.
  Carries all per-association limits such as fairshare, max jobs, max TRES
  per job, and wall duration. Created when an allocation is requested.
- **SlurmUser** — Tracks each user's default account per cluster. One
  record per user per cluster.

## Sync Mechanism

The Slurm integration uses a hybrid approach:

1. **Targeted handlers** — When an allocation is activated, the system
   creates associations for all project users on that allocation's
   account and partition. When an allocation expires or is revoked,
   the system removes those associations and kills running jobs.

2. **Periodic batch sync** — A scheduled job runs a full reconciliation
   using `POST /slurmdb/{version}/config` to upsert the complete
   accounting state. This catches changes that targeted handlers missed.

## REST API

The integration communicates with `slurmrestd` over HTTP using JWT
authentication. Each cluster has connection settings defined in the
Django configuration. The client supports API versions v0.0.41 through
v0.0.45 with a single set of serializers.

## Dump Generation

ColdFront can generate Slurm association dump files compatible with
`sacctmgr dump`. The dump maps ColdFront models to Slurm's association
hierarchy format with cluster headers, account lines, and user lines.
