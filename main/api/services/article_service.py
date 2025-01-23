from ...exceptions import ValidationError, NotFoundError, PermissionError

class ArticleService:
    def __init__(self, repository):
        self.repository = repository

    def get_articles(self, filters=None, user=None):
        if not user or not user.is_authenticated:
            raise PermissionError("Dostęp tylko dla zalogowanych użytkowników")
        return self.repository.get_filtered_articles(filters)

    def create_article(self, article_data, author):
        if not author.is_staff:
            raise PermissionError("Tylko administrator może dodawać artykuły")
        return self.repository.create_article(article_data)

    def update_article(self, article_id, article_data, author):
        if not author.is_staff:
            raise PermissionError("Tylko administrator może edytować artykuły")
        return self.repository.update_article(article_id, article_data)

    def delete_article(self, article_id, author):
        if not author.is_staff:
            raise PermissionError("Tylko administrator może usuwać artykuły")
        self.repository.delete_article(article_id)

    def search_articles(self, search_params):
        if not search_params:
            return self.repository.get_all()
        return self.repository.search_articles(**search_params)