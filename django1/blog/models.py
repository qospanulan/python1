from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    """
    найти посты которые были обновлены спустя 15 минут после создания:

    update_at > created_at + 15 minutes
    created_at < updated_at - 15 minutes

    """
    title = models.CharField(max_length=200)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, related_name="liked_posts")

    tags = models.ManyToManyField(Tag, related_name="posts")

    def __str__(self):
        return f"{self.title} ({self.pk})"  # primary key


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

    def __str__(self):
        return f"{self.text} ({self.pk})"


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.CharField(db_index=True)
    phone_number = models.CharField()

    experience_in_years = models.PositiveIntegerField()
    about = models.TextField()

    class Meta:
        db_table="profiles"
        ordering = ['-experience_in_years']

        unique_together = [('email', 'phone_number')]

