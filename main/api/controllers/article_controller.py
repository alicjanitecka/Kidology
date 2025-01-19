from rest_framework import status
from rest_framework.response import Response
from main.api.serializers.article_serializer import ArticleSerializer
from ...exceptions import ValidationError, NotFoundError, PermissionError
class ArticleController:
    def __init__(self, service):
        self.service = service

    def get_articles(self, request):
        articles = self.service.get_all_articles()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def get_article(self, request, article_id):
        article = self.service.get_article(article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def create_article(self, request):
        try:
            article = self.service.create_article(request.data, request.user)
            return Response(article, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def update_article(self, request, article_id):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = self.service.update_article(article_id, serializer.validated_data)
            return Response(ArticleSerializer(article).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_article(self, request, article_id):
        self.service.delete_article(article_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
