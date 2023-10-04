from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

# 21.	Customers can browse their own orders
class OrderListTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def setUp(self):
        self.username = "customer1"
        self.user = User.objects.get(username=self.username)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_21_customers_can_view_their_orders(self):
        response = self.client.get('/api/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_order_items = [
            {
                "id": 1,
                "order": 1,
                "menuitem": {
                    "title": "Pizza Margherita",
                    "featured": True,
                    "category": 1
                },
                "quantity": 2,
                "unit_price": "10.00",
                "price": "20.00"
            },
            {
                "id": 2,
                "order": 2,
                "menuitem": {
                    "title": "Pizza Margherita",
                    "featured": True,
                    "category": 1
                },
                "quantity": 2,
                "unit_price": "10.00",
                "price": "20.00"
            }
        ]

        expected_orders = [
            {
                "id": 1,
                "user": 8,
                "delivery_crew": 4,
                "status": True,
                "total": "20.00",
                "date": "2023-10-02",
                "order_items": [expected_order_items[0]]
            },
            {
                "id": 2,
                "user": 8,
                "delivery_crew": None,
                "status": True,
                "total": "20.00",
                "date": "2023-10-02",
                "order_items": [expected_order_items[1]]
            }
        ]

        self.assertEqual(response.data, expected_orders)
