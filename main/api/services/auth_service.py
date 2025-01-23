from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from ...exceptions import ValidationError, AuthenticationError


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user_data):
        if self.repository.get_user_by_email(user_data['email']):
            raise ValidationError("Ten email jest już zarejestrowany")
        return self.repository.create_user(user_data)

    def login_user(self, email, password):
        user = self.repository.get_user_by_email(email)
        if not user or not user.check_password(password):
            raise ValidationError("Niepoprawny email lub hasło")
        return user
