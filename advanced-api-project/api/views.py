from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import PermissionDenied
from . import serializers
from .permissions import IsAdminOrReadOnly
# Generic Views for CRUD on Books

class BookListView(generics.ListAPIView):
    """
    ListView: Retrieve all books.
    Accessible to anyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]



class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieve a single book by ID.
    Accessible to anyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        """
        Customize creation: Only staff can create books.
        """
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff users can create books.")
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        """
        Customize update: Do not allow changing publication year.
        """
        if "publication_year" in serializer.validated_data:
            raise serializers.ValidationError(
                "Publication year cannot be modified after creation."
            )
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Remove a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    
