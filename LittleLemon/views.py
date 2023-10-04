from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        username = serializer.validated_data.get('username')
        try:
            user = User.objects.get(username=username)
            is_part_of_any_group = user.groups.exists()
            is_not_manager = not user.groups.filter(name='Manager').exists()
            if is_part_of_any_group and is_not_manager:
                return Response({'detail': 'You can\'t log in because you are not a Manager.'}, status=status.HTTP_403_FORBIDDEN)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'auth_token': token.key}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'detail': 'User not exists.'}, status=status.HTTP_404_NOT_FOUND)
