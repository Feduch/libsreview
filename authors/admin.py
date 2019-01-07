from django.contrib import admin
from authors.models import Author, Nationality


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rating", "date_update", "date_create", "show_counter")
    search_fields = ("id", "name")
    list_filter = ( "status", )

admin.site.register(Author, AuthorAdmin)


class NationalityAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "nationality", "slug")
    prepopulated_fields = {"slug": ("nationality",)}
    search_fields = ("id", "country", "nationality")


admin.site.register(Nationality, NationalityAdmin)