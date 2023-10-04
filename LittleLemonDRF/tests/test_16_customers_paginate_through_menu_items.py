from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# 16.	Customers can paginate menu items
class MenuItemPaginationTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def setUp(self):
        username = "customer1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_16_customers_can_browse_all_menu_items_with_pagination(self):
        page = 1
        all_results = []

        while True:
            response = self.client.get(f'/api/menu-item/?page={page}')
            self.assertEqual(response.status_code, 200)

            results = response.data['results']
            all_results.extend(results)

            if not response.data['next']:
                break

            page += 1

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

        for index, expected_item in enumerate(expected_menu_items):
            self.assertEqual(expected_item, all_results[index])
