from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# 18.	Customers can add menu items to the cart
class MenuItemCartTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def setUp(self):
        self.username = "customer1"
        self.user = User.objects.get(username=self.username)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_18_customers_can_add_menu_items_to_cart(self):
        data = {
            'menu_item_id': 1
        }

        response = self.client.post('/api/cart/add_item/', data)
        self.assertEqual(response.status_code, 201) 
        
        cart_items = response.data

        pizza_item = next((item for item in cart_items if item["menuitem"]["id"] == 1), None)
        
        self.assertIsNotNone(pizza_item, "Pizza Margherita not found in cart.")

        expected_response = {
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
            "quantity": 3, 
            "unit_price": "10.00",
            "price": "30.00"  
        }

        self.assertEqual(expected_response, pizza_item)

