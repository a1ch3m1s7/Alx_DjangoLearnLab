import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)   
        return Book.objects.filter(author=author)       
    except Author.DoesNotExist:
        return []

# List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


if __name__ == "__main__":
    # Example usage
    print("Books by J.K. Rowling:")
    for book in get_books_by_author("J.K. Rowling"):
        print(f"- {book.title}")

    print("\nBooks in City Library:")
    for book in get_books_in_library("City Library"):
        print(f"- {book.title}")

    print("\nLibrarian of City Library:")
    librarian = get_librarian_for_library("City Library")
    print(librarian.name if librarian else "No librarian assigned")
