from .models import Article

class ArticleRepository:
    def get_articles(self, filters=None):
        queryset = Article.objects.all()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def create_article(self, data):
        return Article.objects.create(**data)

    def update_article(self, article_id, data):
        article = Article.objects.get(id=article_id)
        for key, value in data.items():
            setattr(article, key, value)
        article.save()
        return article

    def delete_article(self, article_id):
        Article.objects.filter(id=article_id).delete()
