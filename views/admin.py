from django.contrib import admin
from views.models import View


class ViewAdmin(admin.ModelAdmin):
    list_display = [f.name for f in View._meta.fields]
    search_fields = ("id", "book__id", "book__title")
    readonly_fields = (
        'author', 'book'
    )

admin.site.register(View, ViewAdmin)