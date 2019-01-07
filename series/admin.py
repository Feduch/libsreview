from django.contrib import admin
from series.models import Series


class SeriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "show_counter", "date_update", "date_create")
    search_fields = ("id", "title")
    list_filter = ("status",)


admin.site.register(Series, SeriesAdmin)