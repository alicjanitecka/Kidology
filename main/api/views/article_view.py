from rest_framework import viewsets
from ..repositories.article_repository import ArticleRepository
from ..services.article_service import ArticleService
from ..controllers.article_controller import ArticleController


class ArticleViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = ArticleRepository()
        service = ArticleService(repository)
        self.controller = ArticleController(service)

    def list(self, request):
        return self.controller.get_articles(request)

    # def retrieve(self, request, pk=None):
    #     return self.controller.get_article(request, pk)

    def create(self, request):
        return self.controller.create_article(request)

    def update(self, request, pk=None):
        return self.controller.update_article(request, pk)

    def destroy(self, request, pk=None):
        return self.controller.delete_article(request, pk)