from rest_framework import serializers
from games.models import Game, WinnerChoices
from othello_users.serialiers import ReadOthelloUserSerializer
from typing import Dict, Any


class GameSerializer(serializers.ModelSerializer):
    """ゲームシリアライザ

    """

    player1 = ReadOthelloUserSerializer(read_only=True)
    player2 = ReadOthelloUserSerializer(read_only=True)
    board = serializers.JSONField(read_only=True)

    class Meta:
        model = Game

        fields = (
            'slug',
            'player1',
            'player2',
            'turn',
            'winner',
            'board',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'slug',
            'player1',
            'player2',
            'turn',
            'winner',
            'board',
            'created_at',
            'updated_at',
        )

        extra_kwargs = {}


class ReadGameSerializer(GameSerializer):
    """読み込み専用ゲームシリアラザ

    """

    class Meta(GameSerializer.Meta):
        read_only_fields = GameSerializer.Meta.fields


class ReversingGameSerializer(GameSerializer):
    """反転処理専用ゲームシリアラザ

    """

    x = serializers.IntegerField(write_only=True, min_value=0)
    y = serializers.IntegerField(write_only=True, min_value=0)

    class Meta(GameSerializer.Meta):
        fields = (
            *GameSerializer.Meta.fields,
            'x',
            'y',
        )
        read_only_fields = GameSerializer.Meta.fields

    def update(self, instance: Game, validated_data: Dict[str, Any]):
        # validate メソットだと instance の情報がないためここで検証
        if not instance.winner == WinnerChoices.EMPTY.value[0]:
            raise serializers.ValidationError('有効な座標ではありません')
        if not instance.valid_reversing(x, y):
            raise serializers.ValidationError('有効な座標ではありません')

        # Todo request の値が None のときに例外を発行
        x = validated_data.pop('x')
        y = validated_data.pop('y')
        instance.reversing(x, y)
        instance.save()
        return instance


class ReadGameListSerializer(serializers.ModelSerializer):
    """読み込み専用ゲーム一覧シリアライザ

    """

    player1 = ReadOthelloUserSerializer(read_only=True)
    player2 = ReadOthelloUserSerializer(read_only=True)
    board = serializers.JSONField(read_only=True)

    class Meta:
        model = Game

        fields = (
            'slug',
            'player1',
            'player2',
            'turn',
            'winner',
            'board',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'slug',
            'player1',
            'player2',
            'turn',
            'winner',
            'board',
            'created_at',
            'updated_at',
        )
