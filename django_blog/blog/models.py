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
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Comment linked to a Post.
    - post: many-to-one relationship with Post
    - author: user who wrote the comment
    - content: comment text
    - created_at: set when created
    - updated_at: set when modified
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Tag(models.Model):
    """
    Simple Tag model. Name is unique so we can get_or_create by name.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name