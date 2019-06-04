from django.apps import AppConfig
from django.db.models.signals import pre_save


class MatchingsConfig(AppConfig):
    name = 'matchings'

    def ready(self):
        from matchings.models import Matching
        pre_save.connect(
            Matching._pre_save_handler,
            sender=Matching
        )
