
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# 6.	Managers can update the item of the day
class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_test6.json']

    def test_6_manager_can_mark_menu_item_as_featured(self):
        username = "manager1"
        user = User.objects.get(username=username)
        self.assertIn("Manager", [group.name for group in user.groups.all()])  # Asegurarse de que el usuario es un Manager
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        menu_item_id = 1 
        patch_data = {
            "featured": True
        }
        response = self.client.patch(f"/api/menu-item/{menu_item_id}/", patch_data, format='json')

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data["featured"])
        
    def test_6b_delivery_crew_cannot_mark_menu_item_as_featured(self):
        username = "delivery1"
        user = User.objects.get(username=username)
        self.assertNotIn("Manager", [group.name for group in user.groups.all()])
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        menu_item_id = 1 
        patch_data = {
            "featured": True
        }
        response = self.client.patch(f"/api/menu-item/{menu_item_id}/", patch_data, format='json')

        self.assertEqual(response.status_code, 403)

        response = self.client.get(f"/api/menu-item/{menu_item_id}/", format='json')
        data = response.json()
        self.assertFalse(data["featured"])