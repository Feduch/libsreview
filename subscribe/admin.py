from django.contrib import admin
from subscribe.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "book", "author", "collection")
    search_fields = ("book__id", "author__id", "collection__id")
    readonly_fields = (
        'author', 'book'
    )


admin.site.register(Subscriber, SubscriberAdmin)
