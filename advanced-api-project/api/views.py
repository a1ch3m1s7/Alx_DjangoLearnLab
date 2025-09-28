from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering, searching, and ordering capabilities.
    
    Default Behavior:
    - Returns all Book instances
    - Supports filtering by publication_year and author
    - Supports search by title
    - Supports ordering by various fields
    
    Endpoint: GET /api/books/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    Default Behavior:
    - Returns a specific Book instance based on primary key
    - Includes nested author information
    
    Endpoint: GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book with custom validation and response handling.
    
    Default Behavior:
    - Creates a new Book instance
    - Performs validation including custom publication_year validation
    - Returns 201 Created on success
    
    Customization:
    - Overrides perform_create to add custom logic before saving
    - Custom response format
    
    Endpoint: POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be used for additional processing before saving.
        """
        # Additional validation or processing can be added here
        instance = serializer.save()
        # Example: Log the creation activity
        print(f"Book '{instance.title}' created by user {self.request.user}")

    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response format.
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
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book with partial update support.
    
    Default Behavior:
    - Updates a specific Book instance based on primary key
    - Supports both PUT (full update) and PATCH (partial update) methods
    - Returns 200 OK on success
    
    Customization:
    - Custom response format
    - Additional validation during update
    
    Endpoint: PUT/PATCH /api/books/<int:pk>/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        """
        instance = serializer.save()
        # Example: Log the update activity
        print(f"Book '{instance.title}' updated by user {self.request.user}")

    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response format.
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
                'data': serializer.data
            }
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book with custom deletion handling.
    
    Default Behavior:
    - Deletes a specific Book instance based on primary key
    - Returns 204 No Content on success
    
    Customization:
    - Custom response format instead of 204 No Content
    - Additional cleanup logic
    
    Endpoint: DELETE /api/books/<int:pk>/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        """
        Custom method called when deleting a book instance.
        """
        # Store information for logging before deletion
        book_title = instance.title
        # Perform the deletion
        instance.delete()
        # Example: Log the deletion activity
        print(f"Book '{book_title}' deleted by user {self.request.user}")

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to provide a more informative response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # Custom response instead of default 204 No Content
        return Response(
            {
                'status': 'success',
                'message': 'Book deleted successfully'
            },
            status=status.HTTP_200_OK
        )


class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their nested books.
    
    Endpoint: GET /api/authors/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with nested books.
    
    Endpoint: GET /api/authors/<int:pk>/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    lookup_field = 'pk'