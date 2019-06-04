from django.apps import AppConfig
from django.db.models.signals import pre_save


class GamesConfig(AppConfig):
    name = 'games'

    def ready(self):
        from games.models import Game
        pre_save.connect(
            Game._pre_save_handler,
            sender=Game
        )
