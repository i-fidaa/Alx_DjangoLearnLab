from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes validation to ensure publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation: publication year cannot be greater than current year.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future (>{current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes nested BookSerializer to display all books written by the author.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
