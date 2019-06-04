from django.contrib import admin
from games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('slug', 'created_at', 'updated_at',)
