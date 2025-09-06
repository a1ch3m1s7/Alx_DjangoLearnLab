from django.urls import path
from . import views


urlpatterns = [
    # Function-based view URL
    path('books/', views.book_list, name='book-list'),
    
    # Class-based view URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    # path('libraries/', views.LibraryListView.as_view(), name='library-list'),
]

