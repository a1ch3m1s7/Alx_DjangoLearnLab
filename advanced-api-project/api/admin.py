from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface configuration for Author model"""
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface configuration for Book model"""
    list_display = ['id', 'title', 'publication_year', 'author']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']