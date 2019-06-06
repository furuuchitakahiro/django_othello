from django.contrib.auth import login
from rest_framework import serializers
from othello_users.models import OthelloUser
from typing import Dict, Any


class OthelloUserSerializer(serializers.ModelSerializer):
    """オセロユーザーシリアライザ

    """

    class Meta:
        model = OthelloUser

        fields = (
            'slug',
            'username',
        )
        read_only_fields = (
            'slug',
        )

        extra_kwargs = {}


class ReadOthelloUserSerializer(OthelloUserSerializer):
    """読み込み専用オセロユーザーシリアライザ

    """

    class Meta(OthelloUserSerializer.Meta):
        read_only_fields = OthelloUserSerializer.Meta.read_only_fields


class CreateOthelloUserSerializer(OthelloUserSerializer):
    """作成専用オセロユーザーシリアライザ

    """

    password = serializers.CharField(min_length=8, max_length=128)
    is_login = serializers.BooleanField(
        help_text='このフィールドが True の場合ユーザー作成と同時にログインも行います',
        write_only=True,
        default=True,
    )

    class Meta(OthelloUserSerializer.Meta):
        fields = (
            *OthelloUserSerializer.Meta.fields,
            'email',
            'password',
            'is_login',
        )

        extra_kwargs = {
            **OthelloUserSerializer.Meta.extra_kwargs,
            'email': {'write_only': True},
        }

    def create(self, validated_data: Dict[str, Any]):
        is_login: bool = validated_data.pop('is_login')
        request: 'rest_framework.request.Request' = \
            self.context.get('request', None)
        user: OthelloUser = OthelloUser.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

        if is_login and request is not None:
            login(request, user)

        return user
