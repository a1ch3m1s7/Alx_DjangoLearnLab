# Retrieve
book = Book.objects.get(id=new_book.id)
print(f"Retrieved book: {book.title} by {book.author}")


// output
Retrieved book: 1984 by George Orwell