from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# 12.	Customers can log in using their username and password and get access tokens
class LittleLemonDRFTests(APITestCase):
    def test_12__customer_can_login(self):
        user_data = {
            "username": "customer3",
            "password": "Little+cust3",
            "email": "customer3@email.com"
        }

        response = self.client.post("/users/", user_data, format='json')
        self.assertEqual(response.status_code, 201)

        expected_response = {
            "email": "customer3@email.com",
            "username": "customer3" 
        }
        self.assertEqual(response.data, expected_response)
        self.assertTrue(User.objects.filter(username="customer3").exists())
        username = "customer3"
        password = "Little+cust3"
        response = self.client.post("/token/login", {"username": username, "password": password})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("auth_token", data)
        