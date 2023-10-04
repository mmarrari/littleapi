from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

class AssignDeliveryCrewTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    def test_7_manager_can_assign_users_to_delivery_crew_group(self):
        username = "manager1"
        user = User.objects.get(username=username)
        self.assertIn("Manager", [group.name for group in user.groups.all()])
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data_to_post = {
            "username": "newdeliverycrew"
        }
        response = self.client.post("/api/groups/delivery-crew/users", data=data_to_post, format='json')
        self.assertEqual(response.status_code, 200)
        
        delivery_user = User.objects.get(username=data_to_post["username"])
        self.assertIn("Delivery Crew", [group.name for group in delivery_user.groups.all()])

    def test_7b_non_manager_cannot_assign_users_to_delivery_crew_group(self):
        username = "delivery2"
        user = User.objects.get(username=username)
        self.assertNotIn("Manager", [group.name for group in user.groups.all()])
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data_to_post = {
            "username": "newdeliverycrew"
        }
        response = self.client.post("/api/groups/delivery-crew/users", data=data_to_post, format='json')
        self.assertEqual(response.status_code, 403)
        
        delivery_user = User.objects.get(username=data_to_post["username"])
        self.assertNotIn("Delivery Crew", [group.name for group in delivery_user.groups.all()])
