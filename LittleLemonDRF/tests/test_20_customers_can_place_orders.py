from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

# 20.	Customers can place orders
class OrderCreationTest(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def setUp(self):
        self.username = "customer1"
        self.user = User.objects.get(username=self.username)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_20_customers_can_place_orders(self):
        response = self.client.post('/api/order/create_from_cart/')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(response.data['user'], 8)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['total'], '28.50')
        self.assertEqual(response.data['order_items'][0]['menuitem']['title'], 'Pizza Margherita')
