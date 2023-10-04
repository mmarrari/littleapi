from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class LittleLemonDRFTests(APITestCase):
    fixtures = ['littlelemon_fixture.json']

    # 2.	You can access the manager group with an admin token
    def test_2_you_can_access_manager_group_with_admin_token(self):
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

    def test_2b_non_admin_cannot_access_manager_group(self):
        username = "manager1"
        user = User.objects.get(username=username)
        self.token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get("/api/groups/manager/users")
        
        self.assertEqual(response.status_code, 403)