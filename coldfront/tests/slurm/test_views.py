# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from coldfront.slurm.models import SlurmCluster, SlurmPartition
from coldfront.utils.testing import ViewTestCases, create_tags


class SlurmClusterTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = SlurmCluster

    @classmethod
    def setUpTestData(cls):

        clusters = (
            SlurmCluster(name="Cluster 1"),
            SlurmCluster(name="Cluster 2"),
            SlurmCluster(name="Cluster 3"),
        )
        for cluster in clusters:
            cluster.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Cluster X",
            "tenant_group": None,
            "tenant": None,
            "description": "A new Slurm cluster",
            "is_allocatable": True,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,description",
            "Cluster 4,Fourth cluster",
            "Cluster 5,Fifth cluster",
            "Cluster 6,Sixth cluster",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{clusters[0].pk},Cluster 7,Seven cluster",
            f"{clusters[1].pk},Cluster 8,Eight cluster",
            f"{clusters[2].pk},Cluster 9,Nine cluster",
        )


class SlurmPartitionTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = SlurmPartition

    @classmethod
    def setUpTestData(cls):

        cluster = SlurmCluster.objects.create(name="Test Cluster")

        partitions = (
            SlurmPartition(name="Partition 1", cluster=cluster),
            SlurmPartition(name="Partition 2", cluster=cluster),
            SlurmPartition(name="Partition 3", cluster=cluster),
        )
        for partition in partitions:
            partition.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "cluster": cluster.pk,
            "name": "Partition X",
            "description": "A new Slurm partition",
            "is_allocatable": True,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "cluster,name,description",
            "Test Cluster,Partition 4,Fourth partition",
            "Test Cluster,Partition 5,Fifth partition",
            "Test Cluster,Partition 6,Sixth partition",
        )

        cls.csv_update_data = (
            "id,cluster,name,description",
            f"{partitions[0].pk},Test Cluster,Partition 7,Seven partition",
            f"{partitions[1].pk},Test Cluster,Partition 8,Eight partition",
            f"{partitions[2].pk},Test Cluster,Partition 9,Nine partition",
        )
