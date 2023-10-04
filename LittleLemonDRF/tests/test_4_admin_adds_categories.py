from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from LittleLemonDRF.models import Category

class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    # 4.	The admin can add categories
    def test_4_admin_can_add_categories(self):
        username = "admin"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        category_data = {
            "slug": "new-category",
            "title": "New Category"
        }

        response = self.client.post("/api/category/", category_data, format='json')

        data = response.json()
        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["slug"], category_data["slug"])
        self.assertEqual(data["title"], category_data["title"])

    def test_4b_non_admin_cannot_add_categories(self):
        username = "manager1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        category_data = {
            "slug": "new-category",
            "title": "New Category"
        }

        response = self.client.post("/api/category/", category_data, format='json')
        
        self.assertEqual(response.status_code, 403)

        category_exists = Category.objects.filter(slug="new-category").exists()
        self.assertFalse(category_exists)