import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author (using filter)
def get_books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


# List all books in a library
def get_books_in_library(library_name):
    return Book.objects.filter(libraries__name=library_name)


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    return Librarian.objects.filter(library__name=library_name).first()


if __name__ == "__main__":
    print("Books by J.K. Rowling:")
    for book in get_books_by_author("J.K. Rowling"):
        print(f"- {book.title}")

    print("\nBooks in City Library:")
    for book in get_books_in_library("City Library"):
        print(f"- {book.title}")

    print("\nLibrarian of City Library:")
    librarian = get_librarian_for_library("City Library")
    print(librarian.name if librarian else "No librarian assigned")