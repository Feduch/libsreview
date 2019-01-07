from django.contrib import admin
from awards.models import Award


class AwardAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")

admin.site.register(Award, AwardAdmin)