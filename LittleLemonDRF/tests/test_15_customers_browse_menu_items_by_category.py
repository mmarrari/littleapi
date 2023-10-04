from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json


# 15.	Customers can browse menu items by category
class MenuItemByCategoryBrowserTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_15_customers_can_browse_menu_items_by_category(self):
        username = "customer1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/menu-item-by-category/')
        self.assertEqual(response.status_code, 200)

        expected_data = [
            {
                "id": 1,
                "title": "Category 1",
                "slug": "category1",
                "menuitems": [
                    {
                        "id": 1,
                        "title": "Pizza Margherita",
                        "price": "10.00",
                        "featured": True
                    },
                    {
                        "id": 2,
                        "title": "Cheeseburger",
                        "price": "8.50",
                        "featured": False
                    }
                ]
            },
        ]

        response_data_as_list = json.loads(json.dumps(response.data))

        for expected_category in expected_data:
            self.assertIn(expected_category, response_data_as_list)

