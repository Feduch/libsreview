from django.contrib import admin
from genres.models import Genre, ParentGenre, GenreNew


# class GenreAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "slug")
#     prepopulated_fields = {"slug": ("title",)}
#     search_fields = ("id", "title")
#
# admin.site.register(Genre, GenreAdmin)


class ParentGenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")

admin.site.register(ParentGenre, ParentGenreAdmin)


class GenreNewAdmin(admin.ModelAdmin):
    list_display = ("id", "parent", "name", "slug", "flibusta_id", "genre_litres")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("id", "name")

admin.site.register(GenreNew, GenreNewAdmin)
