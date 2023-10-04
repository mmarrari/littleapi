from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# 17.	Customers can sort menu items by price
class MenuItemOrderingTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def setUp(self):
        username = "customer1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_17_customers_can_sort_menu_items_by_price(self):
        response = self.client.get('/api/menu-item/', {'ordering': 'price'})
        self.assertEqual(response.status_code, 200)

        expected_menu_items_ordered_by_price = [
            {
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
            {
                "id": 1,
                "title": "Pizza Margherita",
                "price": "10.00",
                "featured": True,
                "category": {
                    "id": 1,
                    "slug": "category1",
                    "title": "Category 1"
                }
            }
        ]

        results = response.data['results']

        for index, expected_item in enumerate(expected_menu_items_ordered_by_price):
            self.assertEqual(expected_item, results[index])
