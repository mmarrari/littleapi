from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# 14.	Customers can browse all the menu items at once
class MenuItemBrowserTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_14_customers_can_browse_all_menu_items(self):
        username = "customer1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/menu-item/')
        self.assertEqual(response.status_code, 200)
        expected_menu_items = [
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
            },
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
            }
        ]

        results = response.data['results']

        for expected_item in expected_menu_items:
            self.assertIn(expected_item, results)