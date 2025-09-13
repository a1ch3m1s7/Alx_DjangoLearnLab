from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book, Author

from .forms import ExampleForm


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect("book_list")
    return render(request, "bookshelf/create_book.html")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.save()
        return redirect("book_list")
    return render(request, "bookshelf/edit_book.html", {"book": book})


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("book_list")

def example_view(request):
     if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Save book to database
            return render(request, "bookshelf/form_example.html", {
                "form": BookForm(),  # reset form after submission
                "success": True,
                "title": form.cleaned_data["title"],
                "author": form.cleaned_data["author"],
            })
    else:
        form = BookForm()

    return render(request, "bookshelf/form_example.html", {"form": form})