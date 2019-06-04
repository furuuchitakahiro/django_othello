from enum import Enum, unique
from random import random
from typing import Optional
import secrets


def generate_uniq_slug(
    model_class: 'django.db.models.Model',
    field_name: str,
    length: int = 10
) -> str:
    """ユニークなスラグを生成

    Args:
        model_class ('django.db.models.Model'): モデルクラス
        field_name (str): スラグのフィールド名
        length (int): スラグの長さ ( default 50 )

    Returns:
        str: ユニークなスラグ

    """
    slug = secrets.token_hex(length)[0:length]
    query_args = {
        field_name: slug
    }
    qs_exists = model_class.objects.filter(**query_args).exists()

    # スラグがかぶっていたらループする
    while(qs_exists):
        slug = secrets.token_hex(length)[0:length]
        qs_exists = model_class.objects.filter({
            field_name: slug
        }).exists()

    return slug


@unique
class PlayerChoices(Enum):
    """turn チョイスフィールドの列挙

    """

    PLAYER1 = ('player1', 'player1')
    PLAYER2 = ('player2', 'player2')

    @classmethod
    def get_max_length(cls) -> int:
        return 10

    @classmethod
    def get_random_player(cls) -> str:
        """プレイヤー 1 か 2 どちらかをランダムで取得

        Returns:
            str: プレイヤー

        """
        if random() >= 0.5:
            return cls.PLAYER1.value[0]
        return cls.PLAYER2.value[0]

    @classmethod
    def get_enemy_player(cls, player: str) -> Optional[str]:
        """指定された相手プレイヤーを取得

        Args:
            player (str): プレイヤー

        Returns:
            Optional[str]: 指定されたプレイヤーから見た相手プレイヤー

        """
        if player == cls.PLAYER1.value[0]:
            return cls.PLAYER2.value[0]
        elif player == cls.PLAYER2.value[0]:
            return cls.PLAYER1.value[0]
        return None
