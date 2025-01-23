from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.mixins import UserPassesTestMixin
from ...exceptions import ValidationError


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class AuthController:
    def __init__(self, service):
        self.service = service

    def login(self, request):
        try:
            user = self.service.login_user(
                request.data.get('email'),
                request.data.get('password')
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
            })
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        try:
            user = self.service.register_user({
                'username': request.data.get('username'),
                'email': request.data.get('email'),
                'password': request.data.get('password')
            })
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

