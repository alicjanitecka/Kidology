from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from ...exceptions import ValidationError, AuthenticationError


class AuthService:
    def __init__(self, repository):
        self.repository = repository

    def _validate_email(self, email):
        """Walidacja adresu email"""
        try:
            validate_email(email)
            return True
        except DjangoValidationError:
            return False

    def _validate_password(self, password, password2):
        """Walidacja hasła"""
        if password != password2:
            return False
        if len(password) < 8:
            return False
        return True
    def register_user(self, user_data):
        """
        Rejestracja nowego użytkownika z walidacją danych
        """
        if not self._validate_email(user_data['email']):
            raise ValidationError("Niepoprawny format adresu e-mail")

        if not self._validate_password_strength(user_data['password']):
            raise ValidationError("Hasło musi mieć minimum 8 znaków")

        if user_data['password'] != user_data['password2']:
            raise ValidationError("Hasła nie są identyczne")

        if self.repository.get_user_by_email(user_data['email']):
            raise ValidationError("Ten email jest już zarejestrowany")

        return self.repository.create_user(user_data)

    def login_user(self, email, password):
        """
        Logowanie użytkownika z weryfikacją danych
        """
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValidationError("Niepoprawny email lub hasło")

        if not self.repository.verify_password(user, password):
            self._log_failed_login_attempt(email)
            raise ValidationError("Niepoprawny email lub hasło")

        self._update_last_login(user)
        return user

    def _log_failed_login_attempt(self, email):
        """
        Logowanie nieudanych prób logowania
        """
        self.repository.log_login_attempt(email, success=False)

    def _update_last_login(self, user):
        """
        Aktualizacja czasu ostatniego logowania
        """
        user.last_login = datetime.now()
        self.repository.update_user(user)

    def _validate_password_strength(self, password):
        """
        Sprawdzanie siły hasła
        """
        if len(password) < 8:
            return False
        # Tutaj możesz dodać więcej reguł walidacji hasła
        return True

