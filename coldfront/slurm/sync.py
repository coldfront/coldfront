# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

"""
Slurm sync engine.

Provides the core synchronization logic between ColdFront's local models
and the Slurm REST API (``slurmrestd``).  Three entry points:

* ``run_sync()`` — full reconciliation sync for one or all clusters.
* ``enqueue_activate_allocation()`` — targeted handler for allocation
  activation.
* ``enqueue_deactivate_allocation()`` — targeted handler for allocation
  expire / revoke.
* ``enqueue_remove_project_user()`` — targeted handler for ProjectUser
  deletion.

The ``enqueue_*()`` wrappers are thin — they check the auto-sync gate and
delegate to the task queue.  The actual REST API logic lives in the
corresponding ``_run_*()`` functions so that the CLI command can call them
directly without going through the queue.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from django.conf import settings
from django.utils import timezone

from coldfront.core.models import Job
from coldfront.ras.choices import AllocationStatusChoices
from coldfront.ras.models import Allocation, ProjectUser
from coldfront.slurm.client import SlurmClient
from coldfront.slurm.client.exceptions import (
    SlurmAlreadyExistsException,
)
from coldfront.slurm.models import (
    SlurmAccount,
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmUser,
)

__all__ = (
    "SyncReport",
    "run_sync",
    "enqueue_activate_allocation",
    "enqueue_deactivate_allocation",
    "enqueue_remove_project_user",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# SyncReport
# ---------------------------------------------------------------------------


@dataclass
class SyncReport:
    """Detailed report returned by sync operations."""

    cluster: str
    success: bool = False
    accounts_created: int = 0
    accounts_deleted: int = 0
    associations_created: int = 0
    associations_updated: int = 0
    associations_deleted: int = 0
    users_created: int = 0
    users_updated: int = 0
    users_deleted: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    duration_ms: int = 0


# ---------------------------------------------------------------------------
# SlurmClient factory
# ---------------------------------------------------------------------------


def _build_client(cluster: SlurmCluster | None = None) -> SlurmClient | None:
    """Build a :class:`SlurmClient` from Django settings.

    Looks up the cluster's name in ``settings.SLURMRESTD_CLUSTERS``.
    Falls back to the ``"default"`` entry when the cluster is not listed
    or when ``cluster`` is ``None``.

    Returns ``None`` if slurmrestd is not configured (empty URL).
    """
    clusters_config = getattr(settings, "SLURMRESTD_CLUSTERS", {})

    # Resolve config dict for this cluster (or "default")
    key = cluster.name if cluster is not None else "default"
    config = clusters_config.get(key) or clusters_config.get("default", {})

    url = config.get("url", "")
    if not url:
        return None

    jwt = config.get("jwt_token", "")
    version = config.get("api_version", "") or None
    timeout = config.get("timeout", 30)
    retries = config.get("retries", 3)
    backoff = config.get("retry_backoff", 1.5)

    client = SlurmClient(
        base_url=url,
        jwt_token=jwt,
        version=version,
        timeout=timeout,
        retries=retries,
        retry_backoff=backoff,
    )

    if version is None:
        try:
            client.discover_version()
        except RuntimeError:
            logger.warning("Slurm API version discovery failed — client will not be usable")
            return None

    return client


# ---------------------------------------------------------------------------
# Auto-sync gate
# ---------------------------------------------------------------------------


def _auto_sync_enabled(cluster: SlurmCluster | None = None) -> bool:
    """Return ``True`` if automated Slurm sync is enabled.

    Checks the cluster's config in ``settings.SLURMRESTD_CLUSTERS`` first;
    falls back to the ``"default"`` entry when the cluster is not listed
    or when ``cluster`` is ``None``.
    """
    clusters_config = getattr(settings, "SLURMRESTD_CLUSTERS", {})
    key = cluster.name if cluster is not None else "default"
    config = clusters_config.get(key) or clusters_config.get("default", {})
    return config.get("auto_sync_enabled", False)


# ---------------------------------------------------------------------------
# Targeted handler wrappers (enqueue helpers)
# ---------------------------------------------------------------------------


def enqueue_activate_allocation(allocation_id: int, cluster_id: int | None = None) -> None:
    """Enqueue a targeted task to create associations for an allocation.

    Called by the ViewFlow callback when an allocation is activated.
    Respects the per-cluster ``auto_sync_enabled`` gate — if ``cluster_id``
    is provided, checks that cluster's setting; otherwise checks the
    ``"default"`` cluster config.

    The actual work is done by :func:`_run_activate_allocation` in the
    worker process.
    """
    cluster = SlurmCluster.objects.get(pk=cluster_id) if cluster_id is not None else None
    if not _auto_sync_enabled(cluster):
        logger.debug(
            "Slurm auto sync disabled — skipping activate enqueue for allocation %s",
            allocation_id,
        )
        return

    logger.info("Enqueuing Slurm activate for allocation %s", allocation_id)
    Job.enqueue(
        "coldfront.slurm.sync._run_activate_allocation",
        args=(),
        kwargs={"allocation_id": allocation_id},
        priority=3,
    )


def enqueue_deactivate_allocation(allocation_id: int, cluster_id: int | None = None) -> None:
    """Enqueue a targeted task to remove associations for an allocation.

    Called by ViewFlow callbacks when an allocation is expired or revoked.
    Respects the per-cluster ``auto_sync_enabled`` gate — if ``cluster_id``
    is provided, checks that cluster's setting; otherwise checks the
    ``"default"`` cluster config.
    """
    cluster = SlurmCluster.objects.get(pk=cluster_id) if cluster_id is not None else None
    if not _auto_sync_enabled(cluster):
        logger.debug(
            "Slurm auto sync disabled — skipping deactivate enqueue for allocation %s",
            allocation_id,
        )
        return

    logger.info("Enqueuing Slurm deactivate for allocation %s", allocation_id)
    Job.enqueue(
        "coldfront.slurm.sync._run_deactivate_allocation",
        args=(),
        kwargs={"allocation_id": allocation_id},
        priority=3,
    )


def enqueue_remove_project_user(project_id: int, user_id: int, cluster_ids: list[int] | None = None) -> None:
    """Enqueue a targeted task to remove a user from all allocations.

    Called by the ``post_delete`` signal handler when a ProjectUser is
    deleted.  Respects the per-cluster ``auto_sync_enabled`` gate — if
    ``cluster_ids`` is provided, checks each cluster's setting;
    otherwise checks the ``"default"`` cluster config.
    """
    if cluster_ids:
        for cid in cluster_ids:
            try:
                cluster = SlurmCluster.objects.get(pk=cid)
                if _auto_sync_enabled(cluster):
                    break  # at least one cluster has sync enabled
            except SlurmCluster.DoesNotExist:
                continue
        else:
            # no cluster has sync enabled
            logger.debug(
                "Slurm auto sync disabled — skipping remove-project-user enqueue for project %s user %s",
                project_id,
                user_id,
            )
            return
    elif not _auto_sync_enabled():
        logger.debug(
            "Slurm auto sync disabled — skipping remove-project-user enqueue for project %s user %s",
            project_id,
            user_id,
        )
        return

    logger.info(
        "Enqueuing Slurm remove-project-user for project %s user %s",
        project_id,
        user_id,
    )
    Job.enqueue(
        "coldfront.slurm.sync._run_remove_project_user",
        args=(),
        kwargs={
            "project_id": project_id,
            "user_id": user_id,
        },
        priority=3,
    )


# ---------------------------------------------------------------------------
# Targeted handler implementations (called by worker or CLI)
# ---------------------------------------------------------------------------


def _run_activate_allocation(*, allocation_id: int) -> SyncReport:
    """Create Slurm associations for a newly activated allocation.

    Called by the worker process (or directly by CLI).  Builds a minimal
    config payload containing only the entities needed for this allocation
    and sends it via ``POST /config``.
    """
    report = SyncReport(cluster="", success=False)

    try:
        allocation = Allocation.objects.get(pk=allocation_id)
    except Allocation.DoesNotExist:
        report.errors.append(f"Allocation {allocation_id} not found")
        return report

    resource = allocation.resource_object
    if resource is None:
        report.errors.append(f"Allocation {allocation_id} has no resource")
        return report

    # Determine cluster
    if isinstance(resource, SlurmCluster):
        cluster = resource
    elif isinstance(resource, SlurmPartition):
        cluster = resource.cluster
    else:
        report.errors.append(f"Allocation {allocation_id} targets non-slurm resource")
        return report

    report.cluster = cluster.name

    client = _build_client(cluster)
    if client is None:
        report.errors.append("slurmrestd not configured (SLURMRESTD_URL is empty)")
        return report

    # Load SlurmAssociation
    try:
        association = SlurmAssociation.objects.get(allocation=allocation)
    except SlurmAssociation.DoesNotExist:
        report.errors.append(f"No SlurmAssociation for allocation {allocation_id}")
        return report

    slurm_account = association.slurm_account
    if slurm_account is None:
        report.errors.append(f"SlurmAssociation for allocation {allocation_id} has no slurm_account set")
        return report

    # Ensure the account exists in Slurm
    try:
        client.create_accounts(
            [
                {
                    "name": slurm_account.name,
                    "description": slurm_account.description or "",
                    "organization": slurm_account.organization or "",
                }
            ]
        )
        report.accounts_created += 1
    except SlurmAlreadyExistsException:
        report.warnings.append(f"Account '{slurm_account.name}' already exists")
        report.accounts_created += 1  # idempotent — desired state achieved
    except Exception as exc:
        report.errors.append(f"Failed to create account '{slurm_account.name}': {exc}")

    # Create associations and users for each ProjectUser
    project = allocation.project
    for pu in ProjectUser.objects.filter(project=project).select_related("user"):
        user = pu.user
        if user is None:
            continue

        # Ensure SlurmUser exists
        slurm_user = _ensure_slurm_user(user, cluster, slurm_account, association)

        # Build assoc_rec_set entry
        assoc_payload = _build_assoc_payload(association, user, cluster, resource)
        try:
            client.create_associations([assoc_payload])
            report.associations_created += 1
        except SlurmAlreadyExistsException:
            report.associations_updated += 1
        except Exception as exc:
            report.errors.append(f"Failed to create association for {user.username}: {exc}")

        # Ensure user exists in Slurm
        try:
            client.create_users(
                [
                    {
                        "name": user.username,
                        "default": {
                            "account": slurm_user.default_account.name,
                            "wckey": slurm_user.default_wckey or "",
                        },
                    }
                ]
            )
            report.users_created += 1
        except SlurmAlreadyExistsException:
            report.users_updated += 1
        except Exception as exc:
            report.errors.append(f"Failed to create user '{user.username}': {exc}")

    # Trigger slurmctld cache refresh
    _reconfigure(client)

    report.success = len(report.errors) == 0
    return report


def _run_deactivate_allocation(*, allocation_id: int) -> SyncReport:
    """Remove associations and kill jobs for a deactivated allocation.

    Called when an allocation is expired or revoked.
    """
    report = SyncReport(cluster="", success=False)

    try:
        allocation = Allocation.objects.get(pk=allocation_id)
    except Allocation.DoesNotExist:
        report.errors.append(f"Allocation {allocation_id} not found")
        return report

    resource = allocation.resource_object
    if resource is None:
        report.errors.append(f"Allocation {allocation_id} has no resource")
        return report

    if isinstance(resource, SlurmCluster):
        cluster = resource
    elif isinstance(resource, SlurmPartition):
        cluster = resource.cluster
    else:
        report.errors.append(f"Allocation {allocation_id} targets non-slurm resource")
        return report

    report.cluster = cluster.name

    client = _build_client(cluster)
    if client is None:
        report.errors.append("slurmrestd not configured (SLURMRESTD_URL is empty)")
        return report

    try:
        association = SlurmAssociation.objects.get(allocation=allocation)
    except SlurmAssociation.DoesNotExist:
        report.success = True
        return report

    slurm_account = association.slurm_account
    if slurm_account is None:
        report.success = True
        return report

    partition_name = resource.name if isinstance(resource, SlurmPartition) else ""

    # Kill running jobs for each ProjectUser
    project = allocation.project
    for pu in ProjectUser.objects.filter(project=project).select_related("user"):
        user = pu.user
        if user is None:
            continue
        _kill_user_jobs(client, user, slurm_account, partition_name)

        # Delete the association
        delete_params: dict[str, Any] = {
            "account": slurm_account.name,
            "user": user.username,
            "cluster": cluster.name,
        }
        if partition_name:
            delete_params["partition"] = partition_name
        try:
            client.delete_associations(delete_params)
            report.associations_deleted += 1
        except Exception as exc:
            report.errors.append(f"Failed to delete association for {user.username}: {exc}")

        # Reconcile SlurmUser
        _reconcile_slurm_user(user, cluster, slurm_account)

    # Trigger slurmctld cache refresh
    _reconfigure(client)

    report.success = len(report.errors) == 0
    return report


def _run_remove_project_user(*, project_id: int, user_id: int) -> SyncReport:
    """Remove a user from all allocations on a project.

    Called when a ProjectUser record is deleted.
    """
    report = SyncReport(cluster="", success=False)

    try:
        user_model = settings.AUTH_USER_MODEL
        from django.apps import apps

        User = apps.get_model(user_model)
        user = User.objects.get(pk=user_id)
    except Exception as exc:
        report.errors.append(f"User {user_id} not found: {exc}")
        return report

    # Find all active allocations for this project
    project_allocations = Allocation.objects.filter(
        project_id=project_id,
        status=AllocationStatusChoices.STATUS_ACTIVE,
    )

    # Collect unique clusters involved
    clusters_seen: set[int] = set()
    for allocation in project_allocations:
        resource = allocation.resource_object
        if resource is None:
            continue
        if isinstance(resource, SlurmCluster):
            clusters_seen.add(resource.pk)
        elif isinstance(resource, SlurmPartition):
            clusters_seen.add(resource.cluster_id)

    # Use the first cluster for client building (all clusters on a project
    # should share the same slurmrestd, but if they don't, the client will
    # be built from the first cluster's config)
    first_cluster = SlurmCluster.objects.filter(pk__in=clusters_seen).first() if clusters_seen else None
    client = _build_client(first_cluster)
    if client is None:
        report.errors.append("slurmrestd not configured (SLURMRESTD_URL is empty)")
        return report

    # Reload the query (we consumed it above)
    project_allocations = Allocation.objects.filter(
        project_id=project_id,
        status=AllocationStatusChoices.STATUS_ACTIVE,
    )

    for allocation in project_allocations:
        resource = allocation.resource_object
        if resource is None:
            continue

        if isinstance(resource, SlurmCluster):
            cluster = resource
        elif isinstance(resource, SlurmPartition):
            cluster = resource.cluster
        else:
            continue

        if report.cluster == "":
            report.cluster = cluster.name

        try:
            association = SlurmAssociation.objects.get(allocation=allocation)
        except SlurmAssociation.DoesNotExist:
            continue

        slurm_account = association.slurm_account
        if slurm_account is None:
            continue

        partition_name = resource.name if isinstance(resource, SlurmPartition) else ""

        # Kill jobs
        _kill_user_jobs(client, user, slurm_account, partition_name)

        # Delete association
        delete_params: dict[str, Any] = {
            "account": slurm_account.name,
            "user": user.username,
            "cluster": cluster.name,
        }
        if partition_name:
            delete_params["partition"] = partition_name
        try:
            client.delete_associations(delete_params)
            report.associations_deleted += 1
        except Exception as exc:
            report.errors.append(f"Failed to delete association for {user.username}: {exc}")

        # Reconcile SlurmUser
        _reconcile_slurm_user(user, cluster, slurm_account)

    # Trigger slurmctld cache refresh
    _reconfigure(client)

    report.success = len(report.errors) == 0
    return report


# ---------------------------------------------------------------------------
# Full reconciliation sync
# ---------------------------------------------------------------------------


def run_sync(cluster_id: int | None = None) -> list[SyncReport]:
    """Perform a full reconciliation sync for one or all clusters.

    Uses ``POST /slurmdb/{version}/config`` to upsert the full desired
    accounting state for each cluster, then queries Slurm for orphaned
    associations and deletes them.

    Args:
        cluster_id: Optional cluster PK.  If ``None``, syncs all clusters.

    Returns:
        List of ``SyncReport`` — one per cluster processed.
    """
    reports: list[SyncReport] = []

    clusters = SlurmCluster.objects.all()
    if cluster_id is not None:
        clusters = clusters.filter(pk=cluster_id)

    for cluster in clusters:
        client = _build_client(cluster)
        if client is None:
            report = SyncReport(cluster=cluster.name, success=False)
            report.errors.append("slurmrestd not configured (SLURMRESTD_URL is empty)")
            reports.append(report)
            continue
        report = _sync_cluster(client, cluster)
        reports.append(report)

    return reports


def _sync_cluster(client: SlurmClient, cluster: SlurmCluster) -> SyncReport:
    """Sync a single cluster with slurmrestd."""
    start = timezone.now()
    report = SyncReport(cluster=cluster.name, success=False)

    # ---- Step 1: Build the full config payload ----
    config = _build_config_payload(cluster)
    if config is None:
        report.warnings.append(f"Cluster '{cluster.name}' has no active associations — nothing to upsert")
        report.success = True
        report.duration_ms = 0
        return report

    # ---- Step 2: Upsert via POST /config ----
    try:
        resp = client.upsert_config(config)
        report.accounts_created = len(config.get("accounts", []))
        report.associations_created = len(config.get("associations", []))
        report.users_created = len(config.get("users", []))
        report.warnings.extend(resp.get("warnings", []))
    except Exception as exc:
        report.errors.append(f"Config upsert failed: {exc}")
        report.duration_ms = int((timezone.now() - start).total_seconds() * 1000)
        return report

    # ---- Step 3: Find and delete orphaned associations ----
    try:
        existing = client.get_associations(params={"cluster": cluster.name, "with_deleted": "false"})
    except Exception as exc:
        report.errors.append(f"Failed to query existing associations: {exc}")
        report.duration_ms = int((timezone.now() - start).total_seconds() * 1000)
        return report

    # Build set of expected (account, user, partition) tuples from active
    # associations in ColdFront
    expected = _build_expected_tuples(cluster)

    # Delete orphaned associations
    for assoc in existing.get("associations", []):
        acct = assoc.get("account", "")
        user = assoc.get("user", "")
        partition = assoc.get("partition", "")
        key = (acct, user, partition)
        if key in expected:
            continue

        # This association exists in Slurm but has no matching active
        # allocation in ColdFront — delete it
        try:
            delete_params: dict[str, Any] = {
                "account": acct,
                "user": user,
                "cluster": cluster.name,
            }
            if partition:
                delete_params["partition"] = partition
            client.delete_associations(delete_params)
            report.associations_deleted += 1
        except Exception as exc:
            report.errors.append(
                f"Failed to delete orphaned association (account={acct}, user={user}, partition={partition}): {exc}"
            )

    # ---- Step 4: Trigger slurmctld cache refresh ----
    _reconfigure(client)

    report.duration_ms = int((timezone.now() - start).total_seconds() * 1000)
    report.success = len(report.errors) == 0
    return report


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_config_payload(cluster: SlurmCluster) -> dict[str, Any] | None:
    """Build the full ``openapi_slurmdbd_config_resp`` payload for a cluster.

    Returns ``None`` if the cluster has no active associations.
    """
    from coldfront.slurm.dump import _get_active_associations

    active = _get_active_associations(cluster)
    if not active:
        return None

    # Collect unique accounts
    account_ids = set()
    for a in active:
        if a.slurm_account_id:
            account_ids.add(a.slurm_account_id)

    accounts = SlurmAccount.objects.filter(pk__in=account_ids)

    # Collect unique users across all project members
    user_set: set[int] = set()
    for a in active:
        allocation = a.allocation
        if allocation and allocation.project:
            for pu in allocation.project.users.all():
                if pu.user:
                    user_set.add(pu.user.pk)

    users = SlurmUser.objects.filter(
        cluster=cluster,
        user_id__in=user_set,
    ).select_related("user", "default_account")

    # Build association payloads
    assoc_payloads = []
    for a in active:
        allocation = a.allocation
        if not allocation:
            continue
        resource = allocation.resource_object
        if resource is None:
            continue

        for pu in allocation.project.users.all():
            if not pu.user:
                continue
            assoc_payloads.append(_build_assoc_payload(a, pu.user, cluster, resource))

    # Build account payloads
    account_payloads = [
        {
            "name": acct.name,
            "description": acct.description or "",
            "organization": acct.organization or "",
        }
        for acct in accounts
    ]

    # Build user payloads
    user_payloads = []
    for su in users:
        user_payloads.append(
            {
                "name": su.user.username,
                "default": {
                    "account": su.default_account.name,
                    "wckey": su.default_wckey or "",
                },
            }
        )

    # Build cluster payload
    cluster_payload = {
        "name": cluster.name,
    }
    if cluster.default_qos:
        cluster_payload["defaultqos"] = cluster.default_qos.name

    return {
        "clusters": [cluster_payload],
        "accounts": account_payloads,
        "users": user_payloads,
        "associations": assoc_payloads,
    }


def _build_assoc_payload(
    association: SlurmAssociation,
    user: Any,
    cluster: SlurmCluster,
    resource: SlurmCluster | SlurmPartition,
) -> dict[str, Any]:
    """Build an ``assoc_rec_set`` payload entry from ColdFront models."""
    slurm_account = association.slurm_account
    partition_name = resource.name if isinstance(resource, SlurmPartition) else ""

    payload: dict[str, Any] = {
        "account": slurm_account.name if slurm_account else "",
        "user": user.username,
        "cluster": cluster.name,
        "partition": partition_name,
        "fairshare": association.fairshare,
    }

    if association.default_qos:
        payload["defaultqos"] = association.default_qos.name
    if association.parent:
        payload["parent"] = association.parent.name
    if association.max_jobs is not None:
        payload["maxjobs"] = association.max_jobs
    if association.max_submit_jobs is not None:
        payload["maxsubmitjobs"] = association.max_submit_jobs
    if association.max_tres_per_job is not None:
        payload["maxtresperjob"] = association.max_tres_per_job
    if association.max_tres_mins_per_job is not None:
        payload["maxtresminsperjob"] = association.max_tres_mins_per_job
    if association.max_wall_duration_per_job is not None:
        payload["maxwalldurationperjob"] = int(association.max_wall_duration_per_job.total_seconds())

    return payload


def _build_expected_tuples(cluster: SlurmCluster) -> set[tuple[str, str, str]]:
    """Build set of ``(account, user, partition)`` tuples expected in Slurm.

    Only includes active allocations with a non-null slurm_account.
    """
    from coldfront.slurm.dump import _get_active_associations

    expected: set[tuple[str, str, str]] = set()
    for a in _get_active_associations(cluster):
        acct = a.slurm_account
        if acct is None:
            continue
        allocation = a.allocation
        if not allocation:
            continue
        resource = allocation.resource_object
        if resource is None:
            continue
        partition = resource.name if isinstance(resource, SlurmPartition) else ""
        for pu in allocation.project.users.all():
            if pu.user:
                expected.add((acct.name, pu.user.username, partition))
    return expected


def _ensure_slurm_user(
    user: Any,
    cluster: SlurmCluster,
    slurm_account: SlurmAccount,
    association: SlurmAssociation,
) -> SlurmUser:
    """Get or create a SlurmUser record for a user+cluster.

    Uses ``get_or_create`` — existing records are never modified.
    """
    su, _created = SlurmUser.objects.get_or_create(
        user=user,
        cluster=cluster,
        defaults={"default_account": slurm_account},
    )
    return su


def _reconcile_slurm_user(
    user: Any,
    cluster: SlurmCluster,
    removed_account: SlurmAccount,
) -> None:
    """Reconcile a SlurmUser after an association deletion.

    If the removed account was the user's default, find another active
    allocation on this cluster and update the default.  If no active
    allocations remain, delete the SlurmUser entirely.
    """
    try:
        su = SlurmUser.objects.get(user=user, cluster=cluster)
    except SlurmUser.DoesNotExist:
        return

    if su.default_account != removed_account:
        return  # not affected

    # Find another active allocation on this cluster
    from coldfront.slurm.dump import _get_active_associations

    active = _get_active_associations(cluster)
    for a in active:
        allocation = a.allocation
        if not allocation:
            continue
        if allocation.project and allocation.project.users.filter(user=user).exists():
            if a.slurm_account and a.slurm_account != removed_account:
                su.default_account = a.slurm_account
                su.save()
                return

    # No other active allocation found — delete the SlurmUser
    su.delete()


def _kill_user_jobs(
    client: SlurmClient,
    user: Any,
    account: SlurmAccount,
    partition_name: str,
) -> None:
    """Kill all running jobs for a user on a given account+partition."""
    kill_msg: dict[str, Any] = {
        "user_name": user.username,
        "account": account.name,
        "signal": "SIGTERM",
    }
    if partition_name:
        kill_msg["partition"] = partition_name
    try:
        client.kill_jobs(kill_msg)
    except Exception as exc:
        logger.warning(
            "Failed to kill jobs for user %s account %s partition '%s': %s",
            user.username,
            account.name,
            partition_name,
            exc,
        )


def _reconfigure(client: SlurmClient) -> None:
    """Trigger slurmctld to reload its cached association data."""
    try:
        client._request("GET", client._slurm_path("reconfigure/"))
    except Exception as exc:
        logger.warning("Slurmctld reconfigure failed: %s", exc)
