from relationship_app.models import Author, Book, Library

# 1. Query all books by George Orwell
author = Author.objects.get(name="George Orwell")
print("Books by George Orwell:")
for book in author.books.all():
    print(book.title)

# 2. List all books in Central Library
library = Library.objects.get(name="Central Library")
print("\nBooks in Central Library:")
for book in library.books.all():
    print(book.title)

# 3. Retrieve the librarian for a library
librarian = library.librarian
print(f"\nLibrarian of {library.name}: {librarian.name}")
