import django_filters

from django_filters.rest_framework import FilterSet


class PostFilter(FilterSet):
    author_id = django_filters.NumberFilter(lookup_expr='exact')
    tags = django_filters.BaseInFilter(field_name='tags__name')
