from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from caching.base import CachingMixin, CachingManager
from othello_users.models import OthelloUser
from games.models import Game
from othello_utils.models import PlayerChoices, generate_uniq_slug


class MatchingManager(CachingManager):
    """マッチングマネージャー

    """

    def with_related_object(self) -> 'django.db.models.query.QuerySet':
        """関連オブジェクトを含む

        Returns:
            'django.db.models.query.QuerySet': Description of returned object.

        """
        return self \
            .select_related('host') \
            .select_related('gest') \
            .select_related('game')


class Matching(models.Model, CachingMixin):
    """マッチング

    """

    objects = MatchingManager()

    SLUG_LENGTH = 10

    slug = models.SlugField(
        verbose_name='スラグ',
        max_length=SLUG_LENGTH,
        db_index=True,
        allow_unicode=False
    )
    host = models.ForeignKey(
        verbose_name='ホスト',
        to=OthelloUser,
        on_delete=models.CASCADE,
        related_name='+'
    )
    gest = models.ForeignKey(
        verbose_name='ゲスト',
        to=OthelloUser,
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True
    )
    game = models.ForeignKey(
        verbose_name='ゲーム',
        to=Game,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    board_size = models.PositiveIntegerField(
        verbose_name='盤面の大きさ',
        help_text='この数は偶数でなければなりません',
        validators=[MinValueValidator(8), MaxValueValidator(16)],
    )

    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        base_manager_name = 'objects'

    def __str__(self) -> str:
        return self.host.username

    @classmethod
    def _pre_save_handler(
        cls, sender, instance, raw, using, update_fields, *args, **kwargs
    ):
        """保存直前処理

        """
        is_create: bool = instance.id is None

        if is_create:
            instance.slug = generate_uniq_slug(cls, 'slug', cls.SLUG_LENGTH)
            return

        instance.game = Game.objects.create(
            player1=instance.host,
            player2=instance.gest,
            turn=PlayerChoices.get_random_player(),
            board=Game.create_board(instance.board_size),
        )
