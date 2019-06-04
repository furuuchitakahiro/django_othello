from rest_framework import serializers
from matchings.models import Matching
from othello_users.serialiers import ReadOthelloUserSerializer
from games.serializers import ReadGameSerializer
from typing import Dict, Any


class MatchingSerializer(serializers.ModelSerializer):
    """マッチングシリアラザ

    """

    host = ReadOthelloUserSerializer(read_only=True)
    gest = ReadOthelloUserSerializer(read_only=True)
    game = ReadGameSerializer(read_only=True)

    class Meta:
        model = Matching

        fields = (
            'slug',
            'host',
            'gest',
            'game',
            'board_size',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'slug',
            'host',
            'gest',
            'game',
            'created_at',
            'updated_at',
        )

        extra_kwargs = {}


class ReadMatchingSerializer(MatchingSerializer):
    """読み込み専用マッチングシリアライザ

    """

    class Meta(MatchingSerializer.Meta):
        read_only_fields = MatchingSerializer.Meta.fields


class CreateMatchingSerializer(MatchingSerializer):
    """作成専用マッチングシリアラザ

    """

    def validate_board_size(self, value: int):
        if value % 2 != 0:
            raise serializers.ValidationError('偶数のみ指定できます')
        return value

    class Meta(MatchingSerializer.Meta):
        pass

    def create(self, validated_data):
        # Todo request の値が None のときに例外を発行
        request = self.context.get('request', None)
        host: 'othello_users.models.OthelloUser' = request.user
        return super().create({
            **validated_data,
            'host': host,
        })


class UpdateMatchingSerializer(MatchingSerializer):
    """更新専用マッチングシリアラザ

    """

    class Meta(MatchingSerializer.Meta):
        read_only_fields = (
            *MatchingSerializer.Meta.read_only_fields,
            'board_size',
        )

    def update(self, instance: Matching, validated_data: Dict[str, Any]):
        # Todo request の値が None のときに例外を発行
        request = self.context.get('request', None)
        gest: 'othello_users.models.OthelloUser' = request.user

        # instance の値が validate メソッドでは取れないためここでバリデーション
        if instance.game is not None:
            raise serializers.ValidationError('既にマッチング済みです')
        if gest == instance.host:
            raise serializers.ValidationError('自身とマッチングできません')

        return super().update(instance, {
            **validated_data,
            'gest': gest,
        })


class ReadMatchingListSerializer(serializers.ModelSerializer):
    """読み込み専用マッチング一覧シリアラザ

    """

    host = ReadOthelloUserSerializer(read_only=True)
    gest = ReadOthelloUserSerializer(read_only=True)
    game = ReadGameSerializer(read_only=True)

    class Meta:
        model = Matching

        fields = (
            'slug',
            'host',
            'gest',
            'game',
            'board_size',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields
