from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    # Function-based view URL
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    # path('libraries/', views.LibraryListView.as_view(), name='library-list'),

    # Authentication using Django's built-in views
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Registration (still custom)
    path("register/", views.register_view, name="register")
]

