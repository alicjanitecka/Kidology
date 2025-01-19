
class ValidationError(Exception):
    """Wyjątek dla błędów walidacji"""
    pass

class AuthenticationError(Exception):
    """Wyjątek dla błędów autentykacji"""
    pass

class PermissionError(Exception):
    """Wyjątek dla błędów uprawnień"""
    pass

class NotFoundError(Exception):
    """Wyjątek dla nieznalezionych zasobów"""
    pass
