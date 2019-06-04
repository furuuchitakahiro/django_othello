from django.contrib import admin
from matchings.models import Matching


@admin.register(Matching)
class MatchingAdmin(admin.ModelAdmin):
    list_display = ('slug', 'created_at', 'updated_at',)
