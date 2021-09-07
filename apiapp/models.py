from django.db import models


class Article (models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    email = models.CharField(max_length=155)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
