from django.contrib import admin
from publications.models import Publication


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user")
    search_fields = ("id", "title")
    readonly_fields = (
        'author', 'book', 'series'
    )

admin.site.register(Publication, PublicationAdmin)