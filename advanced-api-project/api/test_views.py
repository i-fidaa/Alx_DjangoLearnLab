from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Unit tests for Book API endpoints.
    Covers CRUD, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="user", password="userpass"
        )

        # Create test author and book
        self.author = Author.objects.create(name="George Orwell")
        self.book = Book.objects.create(
            title="1984", publication_year=1949, author=self.author
        )

        # Endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book.id])
        self.delete_url = reverse("book-delete", args=[self.book.id])


    # Public (Read-Only) Endpoints

    def test_list_books(self):
        """Anyone can view the book list"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("1984", str(response.data))

    def test_detail_book(self):
        """Anyone can view a single book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")

    
    # Authenticated CRUD Endpoints
    
    def test_create_book_requires_staff(self):
        """Only staff can create books"""
        self.client.login(username="user", password="userpass")
        data = {"title": "Animal Farm", "publication_year": 1945, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="admin", password="adminpass")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book_requires_staff(self):
        """Only staff can update books"""
        self.client.login(username="user", password="userpass")
        response = self.client.put(self.update_url, {"title": "Changed", "publication_year": 1949, "author": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="admin", password="adminpass")
        response = self.client.put(self.update_url, {"title": "Changed", "publication_year": 1949, "author": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Changed")

    def test_delete_book_requires_staff(self):
        """Only staff can delete books"""
        self.client.login(username="user", password="userpass")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="admin", password="adminpass")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


    # Filtering, Searching, Ordering

    def test_filter_books_by_year(self):
        """Test filtering books by publication_year"""
        response = self.client.get(self.list_url, {"publication_year": 1949})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """Test searching books by title"""
        response = self.client.get(self.list_url, {"search": "1984"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        """Test ordering books by publication_year"""
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author)
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
