from django.db import models

class Author(models.Model):
    """
    Represents an author who can write multiple books.
    Each author has only a name field for simplicity.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book with title, publication year,
    and a relationship to its author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"  # allows accessing all books from an author (author.books.all())
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
