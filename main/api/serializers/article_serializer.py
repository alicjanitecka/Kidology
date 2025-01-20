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

# class ArticleSerializer(serializers.ModelSerializer):
#     categories = CategorySerializer(many=True, read_only=True)
#     age_groups = AgeGroupSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Article
#         fields = ['id', 'title', 'content', 'categories', 'age_groups', 'created_at', 'updated_at']

class ArticleSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )
    age_groups = serializers.PrimaryKeyRelatedField(
        queryset=AgeGroup.objects.all(),
        many=True
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'categories', 'age_groups', 'created_at', 'updated_at']

class ArticleSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField(required=False)
    search_in_title = serializers.BooleanField(default=True)
    search_in_content = serializers.BooleanField(default=False)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    age_groups = serializers.PrimaryKeyRelatedField(
        queryset=AgeGroup.objects.all(),
        many=True,
        required=False
    )
