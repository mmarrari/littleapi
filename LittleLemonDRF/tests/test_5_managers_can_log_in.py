from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_5_managers_can_log_in(self):
        username = "manager1"
        password = "password123"
        
        user = User.objects.get(username=username)
        self.assertIn("Manager", [group.name for group in user.groups.all()])

        response = self.client.post("/token/login", {"username": username, "password": password})

        self.assertEqual(response.status_code, 201) 
        
        data = response.json()
        self.assertIn("auth_token", data) 

    def test_5b_non_managers_cannot_log_in(self):
        username = "delivery1"
        password = "password123"
        
        user = User.objects.get(username=username)
        self.assertNotIn("Manager", [group.name for group in user.groups.all()])

        response = self.client.post("/token/login", {"username": username, "password": password})

        self.assertEqual(response.status_code, 403)

        data = response.json()
        self.assertNotIn("auth_token", data)