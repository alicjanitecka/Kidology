from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AgeGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category)
    age_groups = models.ManyToManyField(AgeGroup)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.title.strip():
            raise ValidationError("Tytuł nie może być pusty")
        if not self.content.strip():
            raise ValidationError("Treść nie może być pusta")
        if not self.categories.exists():
            raise ValidationError("Artykuł musi mieć przypisaną kategorię")
        if not self.age_groups.exists():
            raise ValidationError("Artykuł musi mieć przypisaną grupę wiekową")

    def get_preview(self):
        words = self.content.split()[:50]
        return ' '.join(words) + '...' if len(self.content.split()) > 50 else self.content
