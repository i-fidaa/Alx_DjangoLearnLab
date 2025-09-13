from django.shortcuts import render

# Create your views here.

from django.views.generic.detail import DetailView
from .models import Library, Book

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view to show details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect("list_books")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, "relationship_app/logout.html")


from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'



@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Book

# Add Book
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author_id")
        publication_year = request.POST.get("publication_year")
        Book.objects.create(title=title, author_id=author_id, publication_year=publication_year)
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')


# Edit Book
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author_id = request.POST.get("author_id")
        book.publication_year = request.POST.get("publication_year")
        book.save()
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {"book": book})


# Delete Book
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {"book": book})
