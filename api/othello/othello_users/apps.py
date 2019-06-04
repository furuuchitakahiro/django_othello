from django.apps import AppConfig
from django.db.models.signals import pre_save


class OthelloUsersConfig(AppConfig):
    name = 'othello_users'

    def ready(self):
        from othello_users.models import OthelloUser
        pre_save.connect(
            OthelloUser._pre_save_handler,
            sender=OthelloUser
        )
