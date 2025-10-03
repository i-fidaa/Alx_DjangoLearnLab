from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag
from .models import Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (e.g. django, tips)."
    )
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]

    def __init__(self, *args, **kwargs):
        # If editing an existing instance, pre-populate the tags field.
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            tag_names = ", ".join([t.name for t in self.instance.tags.all()])
            self.fields['tags'].initial = tag_names

    def save(self, commit=True):
        # Save Post first, then handle tags
        tags_text = self.cleaned_data.pop("tags", "")
        post = super().save(commit=commit)
        # parse tag names, ignore empty names, strip whitespace
        tag_names = [t.strip() for t in tags_text.split(",") if t.strip()]
        tags = []
        for name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag_obj)
        # set many-to-many (clear previous if editing)
        post.tags.set(tags)
        return post


class CommentForm(forms.ModelForm):
    """
    Form for creating/updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content