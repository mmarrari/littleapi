from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from LittleLemonDRF.models import Order


# 8.	Managers can assign orders to the delivery crew
class AssignOrdersToDCrewTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_8_manager_can_assign_delivery_crew(self):
        username = "manager1"
        user = User.objects.get(username=username)
        self.assertIn("Manager", [group.name for group in user.groups.all()])  # Ensure the user is a Manager
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        order_id = 2 
        patch_data = {
            "delivery_crew": 5
        }
        response = self.client.post(f"/api/order/{order_id}/assign_delivery_crew/", patch_data, format='json')

        self.assertEqual(response.status_code, 200)

        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.delivery_crew.id, 5)
        
    def test_8b_delivery_crew_cannot_assign_delivery_crew(self):
        username = "delivery2"
        user = User.objects.get(username=username)
        self.assertNotIn("Manager", [group.name for group in user.groups.all()])  # Ensure the user is not a Manager
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        order_id = 2 
        patch_data = {
            "delivery_crew": 5
        }
        response = self.client.post(f"/api/order/{order_id}/assign_delivery_crew/", patch_data, format='json')

        self.assertEqual(response.status_code, 403)
        order = Order.objects.get(pk=order_id)
        self.assertIsNone(order.delivery_crew)

