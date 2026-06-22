# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0


from coldfront.slurm.models import (
    SlurmAssociation,
    SlurmCluster,
    SlurmPartition,
    SlurmUser,
)


def generate_cluster_dump(cluster):
    """
    Generate Slurm dump content for a given cluster.

    The dump format follows the Slurm dump file format used by sacctmgr:
      - Cluster header line
      - Parent/Account hierarchy lines
      - User lines under each account

    Only active allocations (STATUS_ACTIVE) contribute associations.
    Accounts with no active associations are excluded.

    Args:
        cluster: SlurmCluster instance

    Returns:
        str: The dump file content
    """
    lines = []

    # -- Cluster header --
    cluster_line = _format_cluster(cluster)
    lines.append(cluster_line)
    lines.append("")

    # -- Root account --
    lines.append("Parent - 'root'")
    lines.append("Account - 'root':Fairshare=1:QOS+=normal")
    lines.append("")

    # -- SlurmAccounts with active associations --
    active_assocs = _get_active_associations(cluster)
    accounts_with_assocs = _get_accounts_for_assocs(active_assocs)

    for account in accounts_with_assocs:
        # Find the first association for this account to determine parent
        account_assocs = [a for a in active_assocs if a.slurm_account_id == account.pk]
        if not account_assocs:
            continue

        # Parent line: from association's parent account, or root
        parent_account = account_assocs[0].parent
        if parent_account:
            parent_name = parent_account.name
        else:
            parent_name = "root"
        lines.append(f"Parent - '{parent_name}'")

        # Account line
        account_line = _format_account(account)
        lines.append(account_line)

        # User lines for associations under this account
        for assoc in account_assocs:
            user_lines = _format_user_lines(assoc, cluster)
            lines.extend(user_lines)

        lines.append("")

    return "\n".join(lines)


def _format_cluster(cluster):
    """Format the Cluster header line."""
    parts = [f"Cluster - '{cluster.name}'"]

    # QOS list
    qos_names = _get_qos_names(cluster.qos_list.all())
    if qos_names:
        parts.append(f"QOS+={','.join(qos_names)}")

    # Fairshare
    parts.append(f"Fairshare={cluster.fairshare}")

    # Default QOS
    if cluster.default_qos:
        parts.append(f"DefaultQOS='{cluster.default_qos.name}'")

    return ":".join(parts)


def _format_account(account):
    """Format an Account line."""
    parts = [f"Account - '{account.name}'"]

    # Fairshare — only include if set
    if account.fairshare is not None:
        parts.append(f"Fairshare={account.fairshare}")

    # QOS list
    qos_names = _get_qos_names(account.qos_list.all())
    if qos_names:
        parts.append(f"QOS+={','.join(qos_names)}")

    return ":".join(parts)


def _format_user_lines(assoc, cluster):
    """
    Format User lines for a given association.

    Generates one line per project user in the allocation's project.
    """
    lines = []
    allocation = assoc.allocation
    if not allocation:
        return lines

    project = allocation.project
    if not project:
        return lines

    # Determine resource and QOS list
    resource = allocation.resource_object
    if resource is None:
        return lines

    # Get QOS list from partition or cluster
    if isinstance(resource, SlurmPartition):
        qos_list = resource.qos_list.all()
        partition_name = resource.name
    elif isinstance(resource, SlurmCluster):
        qos_list = resource.qos_list.all()
        partition_name = None
    else:
        # Non-slurm resource — skip
        return lines

    qos_names = _get_qos_names(qos_list)

    # Fairshare logic: if account has fairshare, users inherit via parent
    account = assoc.slurm_account
    if account and account.fairshare is not None:
        fairshare_value = "parent"
    else:
        fairshare_value = assoc.fairshare

    # Get project users
    project_users = project.users.all()

    for pu in project_users:
        user = pu.user
        if not user:
            continue

        # Look up SlurmUser for this user+cluster
        slurm_user = _get_slurm_user(user, cluster)

        # Default account: from SlurmUser, fall back to association account
        if slurm_user and slurm_user.default_account:
            default_acct_name = slurm_user.default_account.name
        elif account:
            default_acct_name = account.name
        else:
            default_acct_name = "root"

        # Build user line
        parts = [f"User - '{user.username}'"]
        parts.append(f"DefaultAccount='{default_acct_name}'")

        # Partition (only if targeting a specific partition)
        if partition_name:
            parts.append(f"Partition='{partition_name}'")

        # Fairshare
        parts.append(f"Fairshare={fairshare_value}")

        # QOS list
        if qos_names:
            parts.append(f"QOS+={','.join(qos_names)}")

        # Limits from association
        limits = _format_limits(assoc)
        if limits:
            parts.extend(limits)

        # Admin level and default WCKey from SlurmUser
        if slurm_user:
            if slurm_user.admin_level and slurm_user.admin_level > 0:
                parts.append(f"AdminLevel='{slurm_user.admin_level}'")
            if slurm_user.default_wckey:
                parts.append(f"DefaultWCKey='{slurm_user.default_wckey}'")

        lines.append(":".join(parts))

    return lines


def _get_slurm_user(user, cluster):
    """Get SlurmUser for the given user and cluster, or None."""
    try:
        return SlurmUser.objects.get(user=user, cluster=cluster)
    except SlurmUser.DoesNotExist:
        return None


def _get_qos_names(qos_list):
    """Return a list of QOS names from a queryset."""
    return [qos.name for qos in qos_list]


def _format_limits(assoc):
    """Format limit fields from a SlurmAssociation into key=value parts."""
    parts = []

    if assoc.max_jobs is not None:
        parts.append(f"MaxJobs={assoc.max_jobs}")

    if assoc.max_submit_jobs is not None:
        parts.append(f"MaxSubmitJobs={assoc.max_submit_jobs}")

    if assoc.max_tres_per_job is not None and assoc.max_tres_per_job != "":
        parts.append(f"MaxTRESPerJob={assoc.max_tres_per_job}")

    if assoc.max_tres_mins_per_job is not None and assoc.max_tres_mins_per_job != "":
        parts.append(f"MaxTRESMinsPerJob={assoc.max_tres_mins_per_job}")

    if assoc.max_wall_duration_per_job is not None:
        # DurationField stores as timedelta; convert to seconds for Slurm
        seconds = int(assoc.max_wall_duration_per_job.total_seconds())
        parts.append(f"MaxWallDurationPerJob={seconds}")

    return parts


def _get_active_associations(cluster):
    """
    Get all SlurmAssociations whose allocations are active and whose
    resource targets the given cluster.

    Returns:
        list of SlurmAssociation (with prefetched allocation, project)
    """
    # Find allocations on this cluster that are active
    from django.contrib.contenttypes.models import ContentType

    from coldfront.ras.choices import AllocationStatusChoices
    from coldfront.ras.models.allocations import Allocation

    cluster_ct = ContentType.objects.get_for_model(SlurmCluster)
    partition_ct = ContentType.objects.get_for_model(SlurmPartition)

    # Allocations targeting this cluster directly
    cluster_allocations = Allocation.objects.filter(
        resource_object_type=cluster_ct,
        resource_object_id=cluster.pk,
        status=AllocationStatusChoices.STATUS_ACTIVE,
    )

    # Allocations targeting partitions that belong to this cluster
    partition_ids = cluster.partitions.values_list("pk", flat=True)
    partition_allocations = Allocation.objects.filter(
        resource_object_type=partition_ct,
        resource_object_id__in=partition_ids,
        status=AllocationStatusChoices.STATUS_ACTIVE,
    )

    # Collect all allocation IDs
    allocation_ids = set(cluster_allocations.values_list("pk", flat=True))
    allocation_ids.update(partition_allocations.values_list("pk", flat=True))

    if not allocation_ids:
        return []

    # Get associations for these allocations
    return list(
        SlurmAssociation.objects.filter(
            allocation_id__in=allocation_ids,
            slurm_account__isnull=False,
        ).select_related("allocation", "slurm_account")
    )


def _get_accounts_for_assocs(assocs):
    """
    Get unique SlurmAccounts referenced by the given associations,
    preserving the order they first appear.
    """
    seen = set()
    accounts = []
    for a in assocs:
        acct = a.slurm_account
        if acct and acct.pk not in seen:
            seen.add(acct.pk)
            accounts.append(acct)
    return accounts
