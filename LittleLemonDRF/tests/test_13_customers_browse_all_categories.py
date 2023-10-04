from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# 13.	Customers can browse all categories 
class CategoryBrowserTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_13_customers_can_browse_all_categories(self):
        username = "customer1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/category/')

        self.assertEqual(response.status_code, 200)

        expected_categories = [
            {"id": 1, "slug": "category1", "title": "Category 1"},
            {"id": 100, "slug": "category100", "title": "Category 100"}
        ]

        for category in expected_categories:
            self.assertIn(category, response.data)
