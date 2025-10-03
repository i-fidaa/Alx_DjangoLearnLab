from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm
from .forms import CommentForm

def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in immediately after registration
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    """Simple profile management (update email only)"""
    if request.method == 'POST':
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        messages.success(request, "Profile updated.")
        return redirect('profile')
    return render(request, 'blog/profile.html', {'user': request.user})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentListView(ListView):
    """
    List comments for a specific post.
    """
    model = Comment
    template_name = "blog/comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__pk=post_id).order_by('created_at')


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a comment for a given post. Requires login.
    """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        # Redirect back to the post detail page after posting a comment
        return reverse('post_detail', args=[self.kwargs.get('post_id')])


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update a comment. Only the comment author may update.
    """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.post.pk])

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment. Only the comment author may delete.
    """
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.post.pk])

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author