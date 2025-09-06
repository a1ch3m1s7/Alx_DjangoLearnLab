from django.urls import path
from .views import list_books


urlpatterns = [
    # Function-based view URL
    path('books/', views.list_books, name='list-books'),
    
    # Class-based view URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    # path('libraries/', views.LibraryListView.as_view(), name='library-list'),
]

