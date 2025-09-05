from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Function-based view
    path("books/", views.list_books, name="list_books"),

    # Class-based view; expects a library ID
    path("library/<int:pk>/", views.libraryDetailView.as_view(), name="library_detail"),

     # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
]
