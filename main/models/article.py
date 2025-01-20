from django.db import models
from .category import Category, AgeGroup

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category)
    age_groups = models.ManyToManyField(AgeGroup)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_preview(self):
        words = self.content.split()[:50]
        return ' '.join(words) + '...' if len(self.content.split()) > 50 else self.content
