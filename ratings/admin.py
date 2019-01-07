from django.contrib import admin
from ratings.models import StarRatings


class StarRatingsAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "author", "collection", "publication", "user", "rating", "date_create")
    search_fields = ("book__id", )
    readonly_fields = (
        'book',
        'author'
    )

admin.site.register(StarRatings, StarRatingsAdmin)