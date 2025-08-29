>>> from bookshelf.models import Book
>>> book = Book(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()
# Output: Book object created successfully with id=1

>>> from bookshelf.models import Book
>>> b = Book.objects.get(title="1984")
>>> print(b.title, b.author, b.publication_year)
# Output: 1984 George Orwell 1949

>>> b.title = "Nineteen Eighty-Four"
>>> b.save()
>>> print(b.title)
# Output: Nineteen Eighty-Four

>>> b.delete()
# Output: (1, {'bookshelf.Book': 1})
>>> Book.objects.all()
# Output: <QuerySet []>
