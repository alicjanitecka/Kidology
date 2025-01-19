from rest_framework import serializers
from main.models import Article, Category, AgeGroup

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    age_groups = AgeGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'categories', 'age_groups', 'created_at', 'updated_at']
