from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Dodatkowe pola, jeśli są potrzebne

    def __str__(self):
        return self.email

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

    def get_preview(self):
        words = self.content.split()[:50]
        return ' '.join(words) + '...' if len(self.content.split()) > 50 else self.content