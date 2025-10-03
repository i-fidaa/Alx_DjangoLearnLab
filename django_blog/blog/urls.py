from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    # List comments for a post
    path("posts/<int:post_id>/comments/", CommentListView.as_view(), name="comment_list"),
    # Create new comment on a post
    path("posts/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    # Update a comment (by comment pk)
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    # Delete a comment (by comment pk)
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]
