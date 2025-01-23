from ...exceptions import ValidationError, NotFoundError, PermissionError
from ..controllers.article_controller import ArticleController
from ...models.article import Article


class ArticleService:
    def __init__(self, repository):
        self.repository = repository

    def _check_admin_permissions(self, user):
        if not user.is_staff:
            raise PermissionError("Tylko administrator może wykonać tę operację")

    def create_article(self, article_data, author):
        self._check_admin_permissions(author)
        return self.repository.create_article(article_data)

    def update_article(self, article_id, article_data, author):
        self._check_admin_permissions(author)
        return self.repository.update_article(article_id, article_data)

    def delete_article(self, article_id, author):
        self._check_admin_permissions(author)
        self.repository.delete(article_id)