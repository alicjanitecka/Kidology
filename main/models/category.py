from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AgeGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
