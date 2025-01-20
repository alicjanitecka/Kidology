from rest_framework import viewsets
from rest_framework.decorators import action
from ..repositories.user_repository import AuthRepository
from ..services.auth_service import AuthService
from ..controllers.auth_controller import AuthController


class AuthViewSet(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = AuthRepository()
        service = AuthService(repository)
        self.controller = AuthController(service)

    @action(detail=False, methods=['post'])
    def login(self, request):
        return self.controller.login(request)

    @action(detail=False, methods=['post'])
    def register(self, request):
        return self.controller.register(request)