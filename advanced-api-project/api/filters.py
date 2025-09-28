import django_filters
from django.db.models import Q
from .models import Book, Author

class BookFilter(django_filters.FilterSet):
    """
    Custom filter set for Book model with advanced filtering capabilities.
    
    Provides filtering on:
    - title (case-insensitive contains)
    - author name (case-insensitive contains)
    - publication_year (exact, range, and comparison filters)
    - publication date range (before and after specific years)
    """
    
    # Basic field filters
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text="Filter books by title (case-insensitive contains)"
    )
    
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter books by author name (case-insensitive contains)"
    )
    
    author_id = django_filters.NumberFilter(
        field_name='author__id',
        help_text="Filter books by specific author ID"
    )
    
    # Publication year filters with multiple lookup expressions
    publication_year = django_filters.NumberFilter(
        help_text="Filter books by exact publication year"
    )
    
    publication_year__gt = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gt',
        help_text="Filter books published after specified year"
    )
    
    publication_year__lt = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lt',
        help_text="Filter books published before specified year"
    )
    
    publication_year__gte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Filter books published in or after specified year"
    )
    
    publication_year__lte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Filter books published in or before specified year"
    )
    
    # Range filter for publication years
    publication_year_range = django_filters.RangeFilter(
        field_name='publication_year',
        help_text="Filter books published within a year range (e.g., publication_year_range=1990&publication_year_range=2000)"
    )
    
    # Custom method filter for complex queries
    search = django_filters.CharFilter(
        method='custom_search',
        help_text="Search across multiple fields (title and author name)"
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'author__name': ['exact', 'icontains'],
        }
    
    def custom_search(self, queryset, name, value):
        """
        Custom search method to search across multiple fields.
        
        Args:
            queryset: The original queryset
            name: Field name (unused in this custom method)
            value: Search term provided by user
            
        Returns:
            QuerySet: Filtered queryset based on search term
        """
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(author__name__icontains=value)
            )
        return queryset
    
    def filter_recent_books(self, queryset, name, value):
        """
        Custom filter to get books published in recent years.
        Example: recent_books=10 (books published in last 10 years)
        """
        if value and value.isdigit():
            from datetime import datetime
            current_year = datetime.now().year
            start_year = current_year - int(value)
            return queryset.filter(publication_year__gte=start_year)
        return queryset

class AuthorFilter(django_filters.FilterSet):
    """
    Custom filter set for Author model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    has_books = django_filters.BooleanFilter(
        method='filter_has_books',
        help_text="Filter authors who have books (true) or no books (false)"
    )
    
    class Meta:
        model = Author
        fields = ['name']
    
    def filter_has_books(self, queryset, name, value):
        """
        Filter authors based on whether they have associated books.
        """
        if value:
            return queryset.filter(books__isnull=False).distinct()
        else:
            return queryset.filter(books__isnull=True)