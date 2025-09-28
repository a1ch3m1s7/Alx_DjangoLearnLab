from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from django_filters import rest_framework
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter, AuthorFilter
from .utils import build_metadata


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', '=title', '^title']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['title']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        if isinstance(response.data, dict):  # paginated
            response.data['metadata'] = build_metadata("book")
        else:  # non-paginated
            response.data = {
                'results': response.data,
                'metadata': build_metadata("book"),
            }
        return response


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()
        related_books = Book.objects.filter(
            author=instance.author
        ).exclude(id=instance.id).only("id", "title", "publication_year")[:5]

        if related_books:
            response.data['related_books'] = BookSerializer(related_books, many=True).data
        return response


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        print(f"Book '{instance.title}' created by {self.request.user}")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                'status': 'success',
                'message': 'Book created successfully',
                'data': serializer.data,
                'links': {
                    'self': request.build_absolute_uri(),
                    'book_detail': request.build_absolute_uri(f"/api/books/{serializer.data['id']}/"),
                    'book_list': request.build_absolute_uri('/api/books/')
                }
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        print(f"Book '{instance.title}' updated by {self.request.user}")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                'status': 'success',
                'message': 'Book updated successfully',
                'data': serializer.data,
                'links': {
                    'self': request.build_absolute_uri(),
                    'book_detail': request.build_absolute_uri(f"/api/books/{serializer.data['id']}/"),
                    'book_list': request.build_absolute_uri('/api/books/')
                }
            }
        )


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        book_title, author_name, book_id = instance.title, instance.author.name, instance.id
        instance.delete()
        print(f"Book '{book_title}' (ID: {book_id}) by {author_name} deleted by {self.request.user}")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_data = BookSerializer(instance).data
        self.perform_destroy(instance)

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
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, dict):  # paginated
            response.data['metadata'] = build_metadata("author")
        else:
            response.data = {
                'results': response.data,
                'metadata': build_metadata("author"),
            }
        return response


class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()
        books_count = instance.books.count()

        response.data['statistics'] = {
            'total_books': books_count,
            'publication_years': list(
                instance.books.order_by('publication_year').values_list('publication_year', flat=True).distinct()
            ) if books_count else []
        }
        return response
