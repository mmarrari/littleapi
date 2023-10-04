from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# 19. Customers can access previously added items in the cart
class CartAccessTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def setUp(self):
        self.username = "customer1"
        self.user = User.objects.get(username=self.username)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_19_customers_can_access_previously_added_items(self):
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, 200)
        
        expected_cart_items = [
            {
                "user": {
                    "id": 8,
                    "username": "customer1",
                    "email": "",
                    "first_name": "",
                    "last_name": ""
                },
                "menuitem": {
                    "id": 1,
                    "title": "Pizza Margherita",
                    "price": "10.00",
                    "featured": True,
                    "category": {
                        "id": 1,
                        "slug": "category1",
                        "title": "Category 1"
                    }
                },
                "quantity": 2,
                "unit_price": "10.00",
                "price": "20.00"
            },
            {
                "user": {
                    "id": 8,
                    "username": "customer1",
                    "email": "",
                    "first_name": "",
                    "last_name": ""
                },
                "menuitem": {
                    "id": 2,
                    "title": "Cheeseburger",
                    "price": "8.50",
                    "featured": False,
                    "category": {
                        "id": 1,
                        "slug": "category1",
                        "title": "Category 1"
                    }
                },
                "quantity": 1,
                "unit_price": "8.50",
                "price": "8.50"
            }
        ]

        for expected_item in expected_cart_items:
            self.assertIn(expected_item, response.data)
