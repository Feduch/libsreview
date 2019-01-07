from django.contrib import admin
from books.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_authors", "date_create", "date_update", "show_counter", "rating", "litres_id", "isbn", "year")
    search_fields = ("id", "title", "original_title", "litres_id", "isbn")
    readonly_fields = (
        'author', 'genre'
    )
    list_filter = ("status",)

admin.site.register(Book, BookAdmin)
