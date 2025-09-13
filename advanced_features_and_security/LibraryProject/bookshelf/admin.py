from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book
from .models import CustomUser, UserProfile
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")   # shows these fields in list view
    list_filter = ("publication_year", "author")             # adds sidebar filters
    search_fields = ("title", "author")                      # adds search box

admin.site.register(Book, BookAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(CustomUser, CustomUserAdmin)