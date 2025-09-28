from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
      """
    BookSerializer serializes all fields of the Book model.
    
    Includes custom validation to ensure publication_year is not in the future.
    
    Fields:
    - id: The primary key of the book
    - title: The title of the book
    - publication_year: The year the book was published
    - author: The foreign key to the Author model
    
    Validation:
    - publication_year cannot be in the future
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation method to ensure publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
     """
    AuthorSerializer serializes Author model with nested book information.
    
    Fields:
    - id: The primary key of the author
    - name: The name of the author
    - books: A nested BookSerializer that dynamically serializes all related books
    
    The relationship between Author and Book is handled through the 'books' field,
    which uses the related_name='books' defined in the Book model's ForeignKey.
    This creates a reverse relationship that allows accessing an author's books.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']