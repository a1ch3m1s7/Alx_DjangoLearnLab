from django.db import models

class Author(models.Model):
     """
    Author model representing a book author.
    
    Fields:
    - name: CharField to store the author's full name
    """
    name = models.CharField(
        max_length=200,
        help_text="The full name of the author"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Book(models.Model):
      """
    Book model representing a published book.
    
    Fields:
    - title: CharField for the book's title
    - publication_year: IntegerField for the year the book was published
    - author: ForeignKey linking to the Author model, establishing a 
      one-to-many relationship (one author can have many books)
    """
    title = models.CharField(
        max_length=200,
        help_text="The title of the book"
    )
    publication_year = models.IntegerField(
        help_text="The year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  
        related_name='books',      
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'author']