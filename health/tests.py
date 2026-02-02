from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError
from unittest import mock


class HealthCheckTests(TestCase):
    def test_health_ok_when_db_is_up(self):
        """
        Health endpoint should return 200 when DB is reachable
        """
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["database"], "up")

    @mock.patch("django.db.connections")
    def test_health_degraded_when_db_is_down(self, mock_connections):
        """
        Health endpoint should return 503 when DB is NOT reachable
        """
        mock_connections.__getitem__.side_effect = OperationalError()

        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["database"], "down")

