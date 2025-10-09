from django.contrib import admin
from .models import RatingChange


@admin.register(RatingChange)
class RatingChangeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rating", "time")
    list_filter = ("time",)
    search_fields = ("user__username",)
    ordering = ("-time",)
