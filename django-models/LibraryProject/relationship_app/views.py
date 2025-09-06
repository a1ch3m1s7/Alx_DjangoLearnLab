from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view: list all books
def book_list(request):
    books = Book.objects.all()
    # Option 1: simple plain text response
    response = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    # Add books to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context