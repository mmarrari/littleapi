from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# 9.	The delivery crew can access orders assigned to them
class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_9_delivery_crew_can_access_order_assigned(self):
        username = "delivery1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.get("/api/order/deliverycrew/", format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)

        orders_ids = [order["id"] for order in data]
        self.assertIn(1, orders_ids)
