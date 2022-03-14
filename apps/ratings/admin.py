from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):

    list_display = ["pkid", "id", "rater", "opponent", "rating"]


admin.site.register(Rating, RatingAdmin)