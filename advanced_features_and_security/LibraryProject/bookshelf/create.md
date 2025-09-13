# create
new_book = Book.objects.create(
    title='1984',
    author='George Orwell',
    publication_year=1949
)
print(f"Created book: {new_book.title}")

// output
Created book: 1984