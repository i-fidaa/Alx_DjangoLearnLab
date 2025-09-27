from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

# Generic Views for CRUD on Books

class BookListView(generics.ListAPIView):
    """
    ListView: Retrieve all books.
    Read-only for everyone, write restricted by permissions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieve a single book by ID.
    Read-only for everyone, write restricted by permissions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Add a new book.
    Restricted to staff users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modify an existing book.
    Restricted to staff users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Remove a book.
    Restricted to staff users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
