from rest_framework import status
from rest_framework.response import Response
from ...exceptions import ValidationError, NotFoundError, PermissionError
from ...models import Article


class ArticleController:
    def __init__(self, service):
        self.service = service

    def _format_article_data(self, article):
        return {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'categories': [c.id for c in article.categories.all()],
            'age_groups': [ag.id for ag in article.age_groups.all()]
        }

    def _handle_error_response(self, error):
        if isinstance(error, ValidationError):
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(error, NotFoundError):
            return Response({'error': str(error)}, status=status.HTTP_404_NOT_FOUND)
        if isinstance(error, PermissionError):
            return Response({'error': str(error)}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_articles(self, request):
        try:
            articles = self.service.get_articles(filters=None, user=request.user)
            return Response({
                'articles': [self._format_article_data(article) for article in articles]
            })
        except Exception as e:
            return self._handle_error_response(e)

    def create_article(self, request):
        try:
            article = Article.objects.create(
                title=request.data.get('title'),
                content=request.data.get('content')
            )

            if 'categories' in request.data:
                article.categories.set(request.data['categories'])
            if 'age_groups' in request.data:
                article.age_groups.set(request.data['age_groups'])

            article.full_clean()

            return Response(
                self._format_article_data(article),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return self._handle_error_response(e)

    def update_article(self, request, article_id):
        try:
            article = self.service.update_article(
                article_id=article_id,
                article_data=request.data,
                author=request.user
            )
            return Response(self._format_article_data(article))
        except Exception as e:
            return self._handle_error_response(e)

    def delete_article(self, request, article_id):
        try:
            self.service.delete_article(article_id, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self._handle_error_response(e)