# Delete the book
book_id = book.id  # Save ID for verification
book.delete()
print(f"Book with ID {book_id} has been deleted")

// output
Book with ID 2 has been deleted