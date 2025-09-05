from django.contrib import admin

# Register your models here.

from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")   # shows these fields in list view
    list_filter = ("publication_year", "author")             # adds sidebar filters
    search_fields = ("title", "author")                      # adds search box

admin.site.register(Book, BookAdmin)
