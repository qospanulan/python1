from django.contrib import admin

from blog.models import Post, Comment, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)

