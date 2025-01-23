from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from ...exceptions import ValidationError, NotFoundError, PermissionError
from ...models import Article


class ArticleController:
    def __init__(self, service):
        self.service = service

    def get_articles(self, request):
        articles = self.service.get_all_articles()
        return Response({
            'articles': [
                {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'categories': [c.id for c in article.categories.all()],
                    'age_groups': [ag.id for ag in article.age_groups.all()]
                } for article in articles
            ]
        })

    def get_article(self, request, article_id):
        article = self.service.get_article(article_id)
        return Response({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'categories': [c.id for c in article.categories.all()],
            'age_groups': [ag.id for ag in article.age_groups.all()]
        })

    def create_article(self, request):
        try:
            with transaction.atomic():
                article = Article.objects.create(
                    title=request.data.get('title'),
                    content=request.data.get('content')
                )

                if 'categories' in request.data:
                    article.categories.add(*request.data['categories'])
                if 'age_groups' in request.data:
                    article.age_groups.add(*request.data['age_groups'])

                return Response({
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'categories': [c.id for c in article.categories.all()],
                    'age_groups': [ag.id for ag in article.age_groups.all()]
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update_article(self, request, article_id):
        try:
            with transaction.atomic():
                article = self.service.get_article(article_id)

                article.title = request.data.get('title', article.title)
                article.content = request.data.get('content', article.content)
                article.save()

                if 'categories' in request.data:
                    article.categories.set(request.data['categories'])
                if 'age_groups' in request.data:
                    article.age_groups.set(request.data['age_groups'])

                return Response({
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'categories': [c.id for c in article.categories.all()],
                    'age_groups': [ag.id for ag in article.age_groups.all()]
                })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete_article(self, request, article_id):
        try:
            self.service.delete_article(article_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
