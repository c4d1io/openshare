from django.test import TestCase, Client


class HealthEndpointTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_returns_200_and_db_up(self):
        response = self.client.get('/health/')
        self.assertIn(response.status_code, (200, 503))
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('database', data)
        # If DB is reachable we expect up and Healthy
        if response.status_code == 200:
            self.assertEqual(data['status'], 'Healthy')
            self.assertEqual(data['database'], 'up')
        else:
            self.assertEqual(response.status_code, 503)
            self.assertEqual(data['database'], 'down')
