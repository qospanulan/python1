from django.forms import ModelForm

from blog.models import Post


class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'author']
