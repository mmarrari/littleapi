from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# 11.	Customers can register
class LittleLemonDRFTests(APITestCase):

    def test_11_register_new_customer(self):
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
