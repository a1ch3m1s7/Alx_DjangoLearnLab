from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for potential ViewSet usage in the future
router = DefaultRouter()
# router.register('books', views.BookViewSet)  # Example for future expansion

urlpatterns = [
    # Include router URLs
    # path('', include(router.urls)),
    
    # Book URLs - Fixed patterns
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    # path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    # path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]

# Optional: API root view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that provides links to all available endpoints.
    """
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'book_create': reverse('book-create', request=request, format=format),
    })

urlpatterns += [
    path('', api_root, name='api-root'),
]