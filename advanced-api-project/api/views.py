"""
Advanced Book API Views with Filtering, Searching, and Ordering

This module implements comprehensive CRUD operations for Book and Author models
with advanced query capabilities using Django REST Framework's generic views
and mixins.

Features Included:
- Complete CRUD operations for Book model
- Advanced filtering using django-filter
- Text search across multiple fields
- Flexible ordering with multi-field support
- Permission-based access control
- Custom response formats with metadata
- Performance optimizations with select_related and prefetch_related

Query Capabilities Examples:
- Filtering: /api/books/?title=harry&author_name=rowling&publication_year__gt=2000
- Searching: /api/books/?search=magic
- Ordering: /api/books/?ordering=-publication_year,title
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter, AuthorFilter


class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for retrieving all books with advanced filtering, 
    searching, and ordering capabilities.
    
    This view provides comprehensive query capabilities allowing API consumers
    to efficiently find and organize book data based on various criteria.
    
    Features:
    - Filtering: Filter by title, author, publication year, and custom ranges
    - Searching: Text search across title and author name fields
    - Ordering: Sort by any book field with multiple field ordering support
    - Pagination: Results paginated with configurable page size
    - Metadata: Detailed information about available query options
    
    Query Parameters Examples:
    
    Filtering: 
        ?title=harry&author_name=rowling&publication_year=1997
        ?publication_year__gt=2000&publication_year__lt=2010
        ?publication_year_range=1990&publication_year_range=2000
    
    Searching:
        ?search=magic
        ?search=rowling
    
    Ordering:
        ?ordering=title
        ?ordering=-publication_year (descending)
        ?ordering=author__name,publication_year (multiple fields)
    
    Combined Usage:
        ?author_name=rowling&search=harry&ordering=-publication_year
    
    Endpoint: GET /api/books/
    Access: Public (read-only)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # DjangoFilterBackend configuration
    filterset_class = BookFilter
    
    # SearchFilter configuration - enables text search across multiple fields
    search_fields = [
        'title',           # Case-insensitive contains search
        'author__name',    # Search in related author names
        '=title',          # Exact match on title
        '^title',          # Starts with title search
    ]
    
    # OrderingFilter configuration - enables dynamic field ordering
    ordering_fields = [
        'title',
        'publication_year', 
        'author__name',
        'id',
    ]
    ordering = ['title']  # Default ordering when no order specified
    
    def get_queryset(self):
        """
        Override to provide additional queryset optimizations and custom filtering.
        
        Returns:
            QuerySet: Optimized queryset with select_related and any custom filters
        """
        queryset = super().get_queryset()
        
        # Example: Custom filtering based on query parameters
        recent_only = self.request.query_params.get('recent_only')
        if recent_only and recent_only.lower() == 'true':
            from datetime import datetime
            current_year = datetime.now().year
            queryset = queryset.filter(publication_year__gte=current_year - 10)
        
        # Example: Custom filter for classic books
        classic_books = self.request.query_params.get('classic_books')
        if classic_books and classic_books.lower() == 'true':
            queryset = queryset.filter(publication_year__lt=1950)
        
        return queryset
    
    def get_ordering(self):
        """
        Custom method to handle complex ordering scenarios and validation.
        
        Returns:
            list: Validated ordering parameters or default ordering
        """
        ordering = self.request.query_params.get('ordering', '').strip()
        
        if not ordering:
            return self.ordering
        
        # Validate ordering fields to prevent SQL injection
        valid_fields = set(self.ordering_fields)
        ordering_fields = [field.strip() for field in ordering.split(',')]
        
        validated_ordering = []
        for field in ordering_fields:
            # Remove descending indicator for validation
            clean_field = field.lstrip('-')
            if clean_field in valid_fields:
                validated_ordering.append(field)
        
        return validated_ordering if validated_ordering else self.ordering
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to include metadata about available filters and options.
        
        Returns:
            Response: Enhanced response with query metadata
        """
        response = super().list(request, *args, **kwargs)
        
        # Add metadata about available filtering, searching, and ordering options
        response.data['metadata'] = {
            'total_count': response.data.get('count', len(response.data.get('results', []))),
            'filtering_options': {
                'title': 'Case-insensitive contains search on book title',
                'author_name': 'Case-insensitive contains search on author name',
                'author_id': 'Exact match on author ID',
                'publication_year': 'Exact publication year',
                'publication_year__gt': 'Books published after specified year',
                'publication_year__lt': 'Books published before specified year',
                'publication_year__gte': 'Books published in or after specified year',
                'publication_year__lte': 'Books published in or before specified year',
                'publication_year_range': 'Books published within year range (min_year&max_year)',
                'search': 'Search across title and author name fields',
                'recent_only': 'Filter books published in last 10 years (true/false)',
                'classic_books': 'Filter books published before 1950 (true/false)',
            },
            'searching_options': {
                'available_fields': ['title', 'author__name'],
                'search_types': ['contains', 'exact', 'starts_with'],
                'examples': [
                    '?search=harry',
                    '?search=rowling',
                    '?search=magic'
                ]
            },
            'ordering_options': {
                'available_fields': ['title', 'publication_year', 'author__name', 'id'],
                'default_ordering': 'title',
                'syntax': 'Prefix with - for descending order',
                'examples': [
                    '?ordering=title',
                    '?ordering=-publication_year',
                    '?ordering=author__name,publication_year'
                ]
            },
            'pagination': {
                'page_size': 20,
                'page_query_param': 'page',
                'max_page_size': 100
            }
        }
        
        return response


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID with optimized database queries.
    
    Uses select_related to include author data in the same database query,
    preventing N+1 query problems and improving performance.
    
    Endpoint: GET /api/books/<int:pk>/
    Access: Public (read-only)
    
    Example:
        GET /api/books/1/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to include additional context or related data.
        """
        response = super().retrieve(request, *args, **kwargs)
        
        # Add related books by same author as additional context
        instance = self.get_object()
        related_books = Book.objects.filter(
            author=instance.author
        ).exclude(id=instance.id)[:5]  # Limit to 5 related books
        
        if related_books:
            related_serializer = BookSerializer(related_books, many=True)
            response.data['related_books'] = related_serializer.data
        
        return response


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book with comprehensive validation.
    
    Includes custom validation for publication_year and custom response formatting.
    Restricted to authenticated users only.
    
    Endpoint: POST /api/books/create/
    Access: Authenticated users only
    
    Example Payload:
        {
            "title": "New Book Title",
            "publication_year": 2023,
            "author": 1
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be used for additional processing before saving.
        
        Args:
            serializer: Validated BookSerializer instance
        """
        # Additional validation or processing can be added here
        instance = serializer.save()
        
        # Example: Log the creation activity
        # In production, you might use Django's logging system
        print(f"Book '{instance.title}' created by user {self.request.user}")
        
        # Example: Send notifications or trigger other actions
        # self.send_creation_notification(instance)

    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response format and add metadata.
        
        Returns:
            Response: Custom response with success status and created data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Custom response with additional context
        return Response(
            {
                'status': 'success',
                'message': 'Book created successfully',
                'data': serializer.data,
                'links': {
                    'self': request.build_absolute_uri(),
                    'book_detail': request.build_absolute_uri(
                        f"/api/books/{serializer.data['id']}/"
                    ),
                    'book_list': request.build_absolute_uri('/api/books/')
                }
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book with partial update support.
    
    Supports both PUT (full update) and PATCH (partial update) methods.
    Includes custom response formatting and restricted to authenticated users.
    
    Endpoint: 
        PUT /api/books/<int:pk>/update/ (full update)
        PATCH /api/books/<int:pk>/update/ (partial update)
    Access: Authenticated users only
    
    Example Payload (PATCH):
        {
            "title": "Updated Book Title"
        }
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        
        Args:
            serializer: Validated BookSerializer instance
        """
        instance = serializer.save()
        
        # Example: Log the update activity
        print(f"Book '{instance.title}' updated by user {self.request.user}")
        
        # Example: Track changes or send notifications
        # self.track_changes(instance, self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response format.
        
        Returns:
            Response: Custom response with success status and updated data
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Custom response with additional context
        return Response(
            {
                'status': 'success',
                'message': 'Book updated successfully',
                'data': serializer.data,
                'links': {
                    'self': request.build_absolute_uri(),
                    'book_detail': request.build_absolute_uri(
                        f"/api/books/{serializer.data['id']}/"
                    ),
                    'book_list': request.build_absolute_uri('/api/books/')
                }
            }
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book with custom deletion handling.
    
    Includes custom response format instead of the default 204 No Content
    and provides informative feedback. Restricted to authenticated users.
    
    Endpoint: DELETE /api/books/<int:pk>/delete/
    Access: Authenticated users only
    
    Example:
        DELETE /api/books/1/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        """
        Custom method called when deleting a book instance.
        
        Args:
            instance: Book instance to be deleted
        """
        # Store information for logging before deletion
        book_title = instance.title
        author_name = instance.author.name
        book_id = instance.id
        
        # Perform the deletion
        instance.delete()
        
        # Example: Log the deletion activity
        print(f"Book '{book_title}' (ID: {book_id}) by {author_name} "
              f"deleted by user {self.request.user}")
        
        # Example: Clean up related resources or send notifications
        # self.cleanup_related_resources(book_id)

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to provide a more informative response.
        
        Returns:
            Response: Custom response with success message instead of 204 No Content
        """
        instance = self.get_object()
        book_data = BookSerializer(instance).data  # Serialize before deletion
        
        self.perform_destroy(instance)
        
        # Custom response instead of default 204 No Content
        return Response(
            {
                'status': 'success',
                'message': 'Book deleted successfully',
                'deleted_book': {
                    'id': book_data['id'],
                    'title': book_data['title'],
                    'author': book_data['author']
                },
                'links': {
                    'book_list': request.build_absolute_uri('/api/books/'),
                    'author_list': request.build_absolute_uri('/api/authors/')
                }
            },
            status=status.HTTP_200_OK
        )


class AuthorListView(generics.ListAPIView):
    """
    Enhanced Author ListView with filtering, searching, and ordering capabilities.
    
    Provides comprehensive query capabilities for author data including
    nested book information through prefetch_related optimization.
    
    Features:
    - Filtering: Filter by author name and book existence
    - Searching: Text search on author names
    - Ordering: Sort by author name or ID
    - Nested Data: Includes related books in response
    
    Query Parameters Examples:
        ?name=rowling
        ?has_books=true
        ?search=king
        ?ordering=name
    
    Endpoint: GET /api/authors/
    Access: Public (read-only)
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to include author-specific metadata.
        """
        response = super().list(request, *args, **kwargs)
        
        # Add author-specific metadata
        response.data['metadata'] = {
            'filtering_options': {
                'name': 'Filter authors by name (case-insensitive contains)',
                'has_books': 'Filter authors who have books (true/false)'
            },
            'searching_options': {
                'available_fields': ['name'],
                'examples': ['?search=rowling', '?search=king']
            },
            'ordering_options': {
                'available_fields': ['name', 'id'],
                'default_ordering': 'name'
            }
        }
        
        return response


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with nested book information.
    
    Uses prefetch_related to efficiently load all related books in a single query,
    preventing N+1 query problems and providing complete author data.
    
    Endpoint: GET /api/authors/<int:pk>/
    Access: Public (read-only)
    
    Example:
        GET /api/authors/1/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to include additional author statistics.
        """
        response = super().retrieve(request, *args, **kwargs)
        
        instance = self.get_object()
        books_count = instance.books.count()
        
        # Add author statistics
        response.data['statistics'] = {
            'total_books': books_count,
            'publication_years': list(
                instance.books.order_by('publication_year')
                .values_list('publication_year', flat=True)
                .distinct()
            ) if books_count > 0 else []
        }
        
        return response


# Optional: API Root View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that provides links to all available endpoints
    with descriptions of their capabilities.
    
    Endpoint: GET /api/
    """
    return Response({
        'books': {
            'url': reverse('book-list', request=request, format=format),
            'description': 'List all books with filtering, searching, and ordering',
            'methods': ['GET'],
            'query_parameters': [
                'filtering (title, author, publication_year)',
                'search (text search across title and author)',
                'ordering (sort by any book field)'
            ]
        },
        'book_create': {
            'url': reverse('book-create', request=request, format=format),
            'description': 'Create a new book (authentication required)',
            'methods': ['POST']
        },
        'authors': {
            'url': reverse('author-list', request=request, format=format),
            'description': 'List all authors with their books',
            'methods': ['GET'],
            'query_parameters': ['filtering', 'search', 'ordering']
        },
        'documentation': {
            'description': 'See README for detailed query examples and usage'
        }
    })