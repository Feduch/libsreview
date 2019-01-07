from django.contrib import admin
from collection.models import Collection


class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user")
    readonly_fields = (
        'book',
    )

admin.site.register(Collection, CollectionAdmin)