from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from games.models import Game
from games.serializers import (
    ReadGameSerializer,
    ReadGameListSerializer,
    ReversingGameSerializer,
)
from games.permissions import IsTurnPlayer
from typing import Optional


class GameViewSets(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """ゲーム API

    """

    lookup_field = 'slug'
    queryset = Game.objects.with_related_object().all()

    def get_serializer_class(self):
        _action = self.action
        serializer_class = ReadGameSerializer

        if _action == 'list':
            serializer_class = ReadGameListSerializer
        elif _action == 'board':
            serializer_class = ReversingGameSerializer

        return serializer_class

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[
            *api_settings.DEFAULT_PERMISSION_CLASSES,
            IsTurnPlayer
        ]
    )
    def board(self, request, slug: Optional[str] = None):
        game = self.get_object()
        serializer = self.get_serializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
