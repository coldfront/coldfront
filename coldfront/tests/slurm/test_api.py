# SPDX-FileCopyrightText: (C) ColdFront Authors
#
# SPDX-License-Identifier: Apache-2.0

from django.urls import reverse

from coldfront.slurm.models import SlurmCluster, SlurmPartition
from coldfront.utils.testing import APITestCase, APIViewTestCases


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("slurm-api:api-root")
        response = self.client.get("{}?format=api".format(url), **self.header)
        self.assertEqual(response.status_code, 200)


class SlurmClusterTest(APIViewTestCases.APIViewTestCase):
    model = SlurmCluster
    brief_fields = ["description", "display", "id", "locked", "name", "url"]
    bulk_update_data = {
        "description": "New description",
    }

    @classmethod
    def setUpTestData(cls):
        clusters = (
            SlurmCluster(name="Cluster 1"),
            SlurmCluster(name="Cluster 2"),
            SlurmCluster(name="Cluster 3"),
        )
        for cluster in clusters:
            cluster.save()

        cls.create_data = [
            {
                "name": "Cluster X",
                "description": "A new Slurm cluster",
                "locked": True,
            },
            {
                "name": "Cluster Y",
                "description": "Another Slurm cluster",
                "locked": True,
            },
            {
                "name": "Cluster Z",
                "description": "Third Slurm cluster",
                "locked": True,
            },
        ]


class SlurmPartitionTest(APIViewTestCases.APIViewTestCase):
    model = SlurmPartition
    brief_fields = ["description", "display", "id", "locked", "name", "url"]
    bulk_update_data = {
        "description": "New description",
    }

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

        cls.create_data = [
            {
                "cluster": cluster.pk,
                "name": "Partition X",
                "description": "A new partition",
                "locked": True,
            },
            {
                "cluster": cluster.pk,
                "name": "Partition Y",
                "description": "Another partition",
                "locked": True,
            },
            {
                "cluster": cluster.pk,
                "name": "Partition Z",
                "description": "Third partition",
                "locked": True,
            },
        ]
