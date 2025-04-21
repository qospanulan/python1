from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes_count = models.PositiveIntegerField(default=0)

    likes = models.ManyToManyField(User, related_name="liked_posts")

    tags = models.ManyToManyField(Tag, related_name="posts")

    def __str__(self):
        return f"{self.title} ({self.pk})"  # primary key


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

    # parent_comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"{self.text} ({self.pk})"

