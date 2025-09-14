from django import forms
from .models import Book

# Example form for creating/editing a book
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]
