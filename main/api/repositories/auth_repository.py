from django.contrib.auth import authenticate
from main.models import CustomUser

class AuthRepository:
    def get_user_by_email(self, email):
        return CustomUser.objects.filter(email=email).first()

    def create_user(self, username, email, password):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user:
            return authenticate(username=user.username, password=password)
        return None
