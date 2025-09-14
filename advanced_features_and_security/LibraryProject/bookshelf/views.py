from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.db.models import Q


# View for listing books (requires can_view permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def search_books(request):
    query = request.GET.get("q", "")
    books = []
    if query:
        # ✅ Safe: ORM query prevents SQL injection
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    return render(request, "bookshelf/book_list.html", {"books": books})