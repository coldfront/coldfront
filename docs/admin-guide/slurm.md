# Slurm Integration

ColdFront integrates with the [Slurm](https://slurm.schedmd.com/) workload
manager to map allocations to Slurm accounting entities. The integration
includes clusters, partitions, accounts, users, associations, and QOS —
matching Slurm's data model and allows for automated provisioning and deprovisioning.

---

## How Slurm Associations Work (Background)

Slurm's accounting data model has four core tables per cluster:

1. **cluster_table** — One row per cluster (name, classification, features).
2. **acct_table** — One row per account (name, description, organization).
   Accounts are lean named containers — no users, no limits.
3. **user_table** — One row per user (name, admin_level). Users are standalone
   entities — no account membership, no limits.
4. **assoc_table** (named `<cluster>_assoc_table`) — The core table. Each row
   represents a **(cluster, account, user, partition)** tuple with a unique
   constraint on `(user, acct, partition)`. This row carries all the limits,
   fairshare shares, QOS references, and hierarchy pointers.

The association is the fundamental entity. An **account-level association**
has `user=""` and serves as a hierarchy parent. A **user-level association**
has both `user="<username>"` and `account="<account>"` and is a leaf node in
the hierarchy tree.

### The Default Account

Every Slurm user has exactly one **default account** per cluster, which is a
property of the user, not the association. The dump format always emits
`:DefaultAccount='<account>'` on every `User -` line because Slurm's parser
requires it — there is no way to emit a user line without specifying a default
account. 

When a user submits a job without specifying `--account=`, Slurm uses the
user's default account. The default account is independent of which
associations the user has — a user can have associations under multiple
accounts while maintaining a single default account.

### Hierarchy

The association hierarchy is built from the `Parent` on the association rows. The
dump format looks like this:

```
Parent - 'root'
Account - 'root':Fairshare=1
    User - 'root':DefaultAccount='root':AdminLevel='Administrator'

Parent - '<account_name>'
Account - '<account_name>':...
    User - '<username>':DefaultAccount='<default_account>':...
    User - '<username>':DefaultAccount='<default_account>':...

Parent - '<parent_account>'
Account - '<child_account>':...
    User - '<username>':DefaultAccount='<default_account>':...
```

Each `Parent -` line sets the hierarchy context for subsequent entities.
Account lines and user lines that follow are children of that parent. The
root account (`root`) is created by default in Slurm and serves as the top
of the hierarchy.

---

## ColdFront Models

### SlurmCluster

Represents a Slurm compute cluster. Allocatable as a resource — allocations
can target a cluster directly (granting access to all partitions) or a
specific partition. Captures the cluster name, tenant, default QOS, QOS
options, fairshare, features, and classification.

### SlurmPartition

Represents a named partition (job submission queue) within a cluster. Also
allocatable as a resource. Captures resource limits (max jobs, TRES, wall
duration), scheduling policies (priority, state, preempt mode, default time),
QOS references (`allow_qos` for admission control, `qos` for limit enforcement),
access restrictions (`allow_groups`, `allow_accounts`), and node configuration.

### SlurmQOS

Represents a Slurm Quality of Service profile. Captures priority, job limits
per user and per account, wall duration limits, limit factor, and grace time.
Referenced by partitions and accounts.

### SlurmAccount

A named Slurm accounting account matching Slurm's `acct_table`. Accounts are
lean containers — just name, cluster, fairshare, and QOS add/remove. All
per-association limits live on `SlurmAssociation` instead.

**Important:** In Slurm, QOS is NOT stored on the account record
(`acct_table` has no `qos` column). QOS lives on the **association**
(`assoc_table`). The `QOS='...'` syntax on account lines in the dump format
is a dump/import convenience that sets QOS on the root association for that
account. ColdFront's `qos_add`/`qos_remove` fields on `SlurmAccount` are a
convenience that propagate QOS to all associations under that account.

### SlurmAssociation

An **allocation extension** that bridges an Allocation to its SlurmAccount.
Created when the allocation is created. Carries all per-association limits
(fairshare, max jobs, max submit jobs, max TRES, max wall duration, QOS
add/remove) and hierarchy pointers (parent account, default QOS). Registered
as an extension for both `SlurmCluster` and `SlurmPartition`.

**Requestable fields** (shown on allocation request and change request forms):
`fairshare`, `max_jobs`, `max_submit_jobs`, `max_wall_duration_per_job`.

**Validation:** When setting `slurm_account`, ColdFront checks for duplicate
`(user, acct, partition)` tuples. Two associations cannot share the same
account for the same partition (or direct-to-cluster scope), which would
create duplicate user association rows in the Slurm dump.

### SlurmUser

Tracks each user's default account per cluster, matching Slurm's
`slurmdb_user_rec_t`. One record per `(user, cluster)` pair. Captures the
user's default account, default wckey, default QOS, and admin level.

**Role in dump generation:** `SlurmUser.default_account` provides the
`:DefaultAccount=` value for all user lines. The association's `slurm_account`
determines which `Account -` hierarchy the user line appears under, but
`DefaultAccount` always comes from `SlurmUser`. This allows a user to have
associations under multiple accounts while maintaining a single default.

---

## Allocation Workflow Integration

Slurm associations and users are created and removed through the allocation
workflow via target callbacks and signal handlers.

### Activation

When an allocation transitions to `active`:

1. **SlurmUser creation** — For each project user, if no `SlurmUser` exists
   for `(user, cluster)`, one is created with `default_account` set to the
   allocation's `slurm_account`. Existing records are never modified.
2. **REST API sync** — A targeted handler creates the account, associations,
   and users in Slurm, then triggers a `slurmctld` cache refresh.
3. **Permission callback** — Blocks activation if the `SlurmAssociation`
   has no `slurm_account` set. An admin must assign the account first.

### Expiration and Revocation

When an allocation transitions to `expired` or `revoked`:

1. **Job termination** — Running jobs for each project user on that
   account+partition are killed via the Slurm REST API.
2. **Association deletion** — User associations are removed from Slurm.
3. **SlurmUser reconciliation** — If the removed account was the user's
   default, another active allocation's account is used. If none remain,
   the `SlurmUser` is deleted.

### ProjectUser Changes

- **User added** — `SlurmUser` records are created or updated.
- **User removed** — Jobs killed, associations deleted, `SlurmUser`
   reconciled, and a targeted handler enqueued for the REST API sync.

---

## Sync Mechanism

ColdFront uses targeted real-time handlers (fired on activate/expire/revoke/
ProjectUser delete) plus a periodic batch sync as a safety net.

### Periodic Batch Sync (Safety Net)

A scheduled job runs full reconciliation for each cluster using
`POST /slurmdb/{version}/config` to upsert the complete accounting state
in a single HTTP call. After the upsert, ColdFront queries Slurm for all
associations, compares against its active associations, and deletes any
orphaned associations that exist in Slurm but have no matching allocation.

This catches drift from manual admin edits and partially-failed targeted
handlers.

### Auto-Sync Gate

Disabled by default per-cluster via `auto_sync_enabled` in
`SLURMRESTD_CLUSTERS`. When disabled, targeted handlers no-op and the batch
job skips that cluster. A CLI command (`coldfront slurm_sync`) is always
available for manual syncs regardless of the setting.

---

## Dump Generation

ColdFront can generate Slurm association dump files compatible with
`sacctmgr dump`. The dump maps ColdFront models to Slurm's association
hierarchy format.

### Dump format rules

- Only **active** allocations (`STATUS_ACTIVE`) contribute associations.
- Accounts with no active associations are excluded.
- `DefaultAccount` always comes from `SlurmUser`, not from the association's
  account. This preserves the user's true default account even when
  associations exist under multiple accounts.
- Fairshare logic: if `SlurmAccount.fairshare` is set, user lines use
  `Fairshare=parent` (inheriting from the account). Otherwise, each user
  line uses its association's `fairshare` value directly.
- QOS list comes from `SlurmPartition.allow_qos` (or `SlurmCluster.qos_list`
  for direct-to-cluster allocations), merged with association-level
  `qos_add`/`qos_remove`.
- Limits (`MaxJobs`, `MaxSubmitJobs`, `MaxTRESPerJob`, etc.) come from the
  `SlurmAssociation`, matching Slurm's model where each assoc row carries
  its own limits.

---

## Fairshare Semantics

Every association in Slurm has a `shares_raw` value that determines relative
priority within the fairshare tree. The normalization algorithm computes a
`shares_norm` for each association by multiplying ratios up the hierarchy.

### How Fairshare=parent Works

When a user association has `Fairshare=parent` it inherits the parent account's
normalized shares directly. In the fair tree algorithm, the user's
`shares_norm` is computed as the parent account's `shares_raw` divided by
the parent's `level_shares` — meaning all users under the same account share
the account's fairshare equally.

**Example:** If an account has `Fairshare=100` and 7 users all have
`Fairshare=parent`, each user gets `100 / 7 ≈ 14.28` normalized shares. The
account's `shares_norm` is `100 / (sum of sibling accounts)`, and users
inherit that value equally.

### Account Fairshare Propagation

When `SlurmAccount.fairshare` is set (not null), **all user associations
under that account use `Fairshare=parent`** in the dump output:

```
Account - 'hpc-lab':Fairshare=100
    User - 'alice':Fairshare=parent   ← inherits from account
    User - 'bob':Fairshare=parent     ← inherits from account
```

If `SlurmAccount.fairshare` is null, each user association falls back to its
own `SlurmAssociation.fairshare` value, written directly as `Fairshare=N`.

### Why ColdFront Defaults to Fairshare=1

All fairshare fields (`SlurmCluster.fairshare`, `SlurmAccount.fairshare`,
`SlurmAssociation.fairshare`) default to `1`. This is deliberate:

1. **`Fairshare=1` produces correct equal-sharing behavior.** All siblings
   with `Fairshare=1` divide their parent's fairshare equally (`1/N` each).
2. **Omitting fairshare would break fairshare entirely.** If fairshare was
   `null` by default, the dump would omit `Fairshare=` for most associations.
   Slurm treats omitted fairshare as `INFINITE` shares — unlimited priority.
3. **Slurm's own default for root accounts is effectively `Fairshare=1`.**
   The root account is hardcoded as `Account - 'root':Fairshare=1`.

---

## AllowQOS vs QOS Precedence

Slurm partitions support two distinct QOS-related directives that are both
present in ColdFront's `SlurmPartition` model.

| Directive | slurm.conf key | ColdFront field | Role |
|-----------|---------------|-----------------|------|
| **AllowQOS** | `AllowQOS=` | `SlurmPartition.allow_qos` (M2M) | **Admission control** — which QOSes are permitted |
| **QOS** | `QOS=` | `SlurmPartition.qos` (FK) | **Limit enforcement** — limits apply to every job |

### AllowQOS (Admission Control)

`AllowQOS` gates whether a job can submit to the partition based on the
**job's QOS** (the QOS the user requests via `--qos=` or inherits from
their association). If the job's QOS is not in the partition's `allow_qos`
list, the job is rejected with an `ESLURM_INVALID_QOS` error.

### QOS (Limit Enforcement)

The partition's QOS (`SlurmPartition.qos`) and the job's QOS are **separate
entities**. Both have their limits enforced on the job. The stricter limit
for any given resource wins.

**Example:** Given `AllowQOS=testA,testB` and `QOS=testC`:
- Only jobs requesting QOS `testA` or `testB` can submit to the partition
- Every job gets limits from **both** `testC` and `testA`/`testB`
- If `testC` has `MaxTime=240:00:00` and `testA` has `MaxTime=120:00:00`,
  the effective limit is `120:00:00` (the stricter one)

### Key Takeaways

- Both the partition QOS and the job's QOS are enforced simultaneously.
  Neither overrides the other.
- If a job's QOS has the `OverPartQOS` flag, the job's QOS becomes primary,
  but the partition QOS is still enforced as secondary.
- `SlurmPartition.qos` (FK) sets the partition-level QOS for limit
  enforcement. `SlurmPartition.allow_qos` (M2M) sets the admission control
  whitelist. They serve different purposes and can be set independently.

---

## REST API Integration

ColdFront communicates with `slurmrestd` over HTTP using JWT authentication.
The client supports API versions v0.0.41 through v0.0.45 with a single set of
serializers — all entity schemas are stable across these versions.

### Connection Configuration

Per-cluster settings are defined in `SLURMRESTD_CLUSTERS`, modeled after
Django's `DATABASES` setting:

```python
SLURMRED_CLUSTERS = {
    "default": {
        "url": "http://slurmrestd:8080",
        "jwt_token": "...",
        "api_version": "v0.0.44",
        "auth_type": "jwt",
        "timeout": 30,
        "retries": 3,
        "retry_backoff": 1.5,
        "auto_sync_enabled": False,
    },
    "hpc01": {
        "url": "http://hpc01-restd:8080",
        "jwt_token": "...",
        "api_version": "v0.0.44",
        "auth_type": "jwt",
        "timeout": 30,
        "retries": 3,
        "retry_backoff": 1.5,
        "auto_sync_enabled": True,
    },
}
```

A `"default"` key provides fallback values for clusters without their own
entry. The JWT token must belong to a Slurm user with
`AdminLevel=Administrator` to have permission to create, update, and delete
all accounting entities.

### Cache Refresh

Writing associations to slurmdbd via the REST API is only half the picture.
Slurm's controller (`slurmctld`) caches association data in memory and does
not poll slurmdbd continuously. After creating or deleting associations,
ColdFront calls `GET /slurm/{version}/reconfigure/` to trigger an immediate
cache refresh so users can submit jobs under their new association without
delay.

---

## Importing Clusters

ColdFront can import cluster configuration from a `slurm.conf` file or the
Slurm REST API, creating `SlurmCluster`, `SlurmPartition`, and `SlurmQOS`
records automatically.

### From slurm.conf

The `coldfront import_slurm_conf <path>` command parses a `slurm.conf` file
and creates matching records in ColdFront. It handles:
- `ClusterName` → `SlurmCluster`
- `PartitionName` → `SlurmPartition` (with nodes, priority, state, QOS refs)
- `QOSName` → `SlurmQOS`
- Default partition templates (`PartitionName=DEFAULT ...`)

Supports `--noop` (dry-run) and `--update` (update existing records) modes.

### From REST API

The `coldfront import_slurm_api <cluster_name>` command fetches partition
info from `slurmctld` and QOS info from `slurmdbd`, creating or updating
records in ColdFront. This is useful when no `slurm.conf` is available or
the running configuration differs from the file.

---

## Permissions and Partition Access

### Default Permissions for Slurm Partitions

The default `slurm.view_slurmpartition` permission grants users access to
partitions based on a set of OR'd conditions:

- Partition is unlocked and has no `allow_groups` or `allow_accounts`
  restrictions (public partitions).
- User is a member of an allowed group (`allow_groups`).
- User has an active allocation with a `SlurmAssociation` under an allowed
  account (`allow_accounts`).
- User has a `SlurmUser` record whose default account is in the partition's
  allowed accounts.

### Default Permissions for Slurm Clusters

The default `slurm.view_slurmcluster` permission grants users access to
unlocked clusters (`{"locked": false}`).
