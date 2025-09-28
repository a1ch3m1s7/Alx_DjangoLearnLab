import django_filters
from .models import Book, Author
from datetime import datetime


class BookFilter(django_filters.FilterSet):
    recent_only = django_filters.BooleanFilter(method='filter_recent')
    classic_books = django_filters.BooleanFilter(method='filter_classics')

    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['icontains'],
            'author': ['exact'],
            'publication_year': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }

    def filter_recent(self, queryset, name, value):
        if value:
            current_year = datetime.now().year
            return queryset.filter(publication_year__gte=current_year - 10)
        return queryset

    def filter_classics(self, queryset, name, value):
        if value:
            return queryset.filter(publication_year__lt=1950)
        return queryset


class AuthorFilter(django_filters.FilterSet):
    has_books = django_filters.BooleanFilter(method='filter_has_books')

    class Meta:
        model = Author
        fields = ['name']

    def filter_has_books(self, queryset, name, value):
        if value:
            return queryset.filter(books__isnull=False).distinct()
        return queryset
