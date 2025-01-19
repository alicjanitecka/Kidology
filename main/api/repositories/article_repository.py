from main.models import Article
from django.shortcuts import get_object_or_404

class ArticleRepository:
    def get_all(self):
        return Article.objects.all()

    def get_by_id(self, article_id):
        return get_object_or_404(Article, id=article_id)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, article, validated_data):
        for attr, value in validated_data.items():
            setattr(article, attr, value)
        article.save()
        return article

    def delete(self, article_id):
        article = self.get_by_id(article_id)
        article.delete()
