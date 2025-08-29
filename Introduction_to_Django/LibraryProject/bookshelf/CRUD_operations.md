>>> from bookshelf.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Output: <Book: 1984>


>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> print(book.title, book.author, book.publication_year)
# Output: 1984 George Orwell 1949


>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> print(book.title)
# Output: Nineteen Eighty-Four


>>> book.delete()
# Output: (1, {'bookshelf.Book': 1})
>>> Book.objects.all()
# Output: <QuerySet []>

