from django.shortcuts import render, redirect
from .forms import ExampleForm
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

def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})