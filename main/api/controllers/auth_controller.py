from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from main.api.serializers.auth_serializer import UserSerializer, LoginSerializer, RegisterSerializer

class AuthController:
    def __init__(self, service):
        self.service = service

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = self.service.login_user(
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = self.service.register_user(
                serializer.validated_data['username'],
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
