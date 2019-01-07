from django.contrib import admin
from user_profile.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("id", "user__id")


admin.site.register(Profile, ProfileAdmin)