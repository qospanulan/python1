import django_filters

from django_filters.rest_framework import FilterSet

from blog.models import Post


class PostFilter(FilterSet):
    author_id = django_filters.NumberFilter(lookup_expr='exact')
    tags = django_filters.BaseInFilter(field_name='tags__name')

    # class Meta:
    #     model = Post
    #     fields = {
    #         'author_id': ['exact'],
    #         'likes_count': ['exact', 'lt', 'gt'],
    #         'tags__name': ['in']
    #     }

