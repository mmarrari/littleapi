from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    # 1.	The admin can assign users to the manager group
    def test_admin_can_assign_users_to_manager_group(self):
        username = "admin"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get("/api/groups/manager/users")
        data = response.json()
        usernames = [user["username"] for user in data]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIn("manager1", usernames)
        self.assertIn("manager2", usernames)
        # Assign new manager
        data_to_post = {
                            "username": "newmanager"
                        }
        response = self.client.post("/api/groups/manager/users", data=data_to_post, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/groups/manager/users")
        data = response.json()
        usernames = [user["username"] for user in data]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertIn("manager1", usernames)
        self.assertIn("manager2", usernames)
        self.assertIn("newmanager", usernames)
        
    def test_1b_non_admin_cannot_assign_users_to_manager_group(self):
        username = "manager1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data_to_post = {
                            "username": "newmanager"
                        }
        response = self.client.post("/api/groups/manager/users", data=data_to_post, format='json')
        
        self.assertEqual(response.status_code, 403)
        
        new_manager = User.objects.get(username="newmanager")
        self.assertNotIn("Manager", [group.name for group in new_manager.groups.all()])
