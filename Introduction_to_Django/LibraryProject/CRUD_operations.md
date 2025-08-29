# create
new_book = Book.objects.create(
    title='1984',
    author='George Orwell',
    publication_year=1949
)
print(f"Created book: {new_book.title}")

// output
Created book: 1984

# Retrieve
book = Book.objects.get(id=new_book.id)
print(f"Retrieved book: {book.title} by {book.author}")


// output
Retrieved book: 1984 by George Orwell

# Update
book.title = 'Nineteen Eighty-Four'
book.save()
print(f"Updated title to: {book.title}")

// output
Updated title to: Nineteen Eighty-Four

# Delete
book_id = book.id  # Save ID for verification
book.delete()
print(f"Book with ID {book_id} has been deleted")

// output
Book with ID 2 has been deleted