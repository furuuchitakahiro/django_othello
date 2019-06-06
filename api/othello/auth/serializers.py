from rest_framework import serializers
from othello_users.serialiers import OthelloUserSerializer


class LoginSerializer(OthelloUserSerializer):
    """ログイン専用シリアラザ

    Notes:
        email フィールドはモデルの設定で unique で設定されていて
            そのまま使うとエラーを出してしまうのであえて定義している

    """

    password = serializers.CharField(
        min_length=8, max_length=128, write_only=True
    )
    email = serializers.EmailField(write_only=True)

    class Meta(OthelloUserSerializer.Meta):
        fields = (
            *OthelloUserSerializer.Meta.fields,
            'email',
            'password',
        )

        read_only_fields = (
            *OthelloUserSerializer.Meta.read_only_fields,
            'username'
        )


class LogoutSerializer(serializers.Serializer):
    """ログアウト専用シリアライザ

    """
    pass
