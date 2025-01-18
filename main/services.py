from .models import Article
from .repositories import ArticleRepository

class ArticleService:
    def __init__(self):
        self.repository = ArticleRepository()

    def get_articles(self, filters=None):
        return self.repository.get_articles(filters)

    def create_article(self, data):
        return self.repository.create_article(data)

    def update_article(self, article_id, data):
        return self.repository.update_article(article_id, data)

    def delete_article(self, article_id):
        return self.repository.delete_article(article_id)
