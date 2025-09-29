from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Post model for blog articles.
    Each post has a title, content, publication date, and an author (linked to Django's User).
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
