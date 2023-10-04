from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    # 3.	The admin can add menu items 
    def test_3_admin_can_add_menu_items(self):
        username = "admin"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        menu_item_data = {
            "title": "Menu Item New",
            "price": "10.00",
            "category_id": 1,
            "featured": False
        }

        response = self.client.post("/api/menu-item/", menu_item_data, format='json')

        data = response.json()
        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["title"], menu_item_data["title"])
        self.assertEqual(data["price"], menu_item_data["price"])
        self.assertFalse(data["featured"])
        self.assertEqual(data["category"]["id"], 1)
        self.assertEqual(data["category"]["slug"], "category1")
        self.assertEqual(data["category"]["title"], "Category 1")

def test_3b_non_admin_cannot_add_menu_items(self):
    username = "manager1"
    user = User.objects.get(username=username)
    self.token, created = Token.objects.get_or_create(user=user)
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    menu_item_data = {
        "title": "Menu Item New",
        "price": "10.00",
        "category_id": 1,
        "featured": False
    }

    response = self.client.post("/api/menu-item/", menu_item_data, format='json')
    
    self.assertEqual(response.status_code, 403)

    response = self.client.get("/api/menu-item/")
    data = response.json()
    titles = [item["title"] for item in data]
    self.assertNotIn("Menu Item New", titles)