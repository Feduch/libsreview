from django.contrib import admin
from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "author", "publication", "collection", "date_create", "user")
    search_fields = ("id", "book__id")
    readonly_fields = (
        'book', 'author'
    )

admin.site.register(Comment, CommentAdmin)