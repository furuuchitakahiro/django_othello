from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from othello_users.models import OthelloUser
from othello_users.serialiers import (
    ReadOthelloUserSerializer,
    CreateOthelloUserSerializer,
)


class OthelloUserViewSets(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """オセロユーザー API

    """

    lookup_field = 'slug'
    queryset = OthelloUser.objects.all()

    def get_serializer_class(self):
        _action = self.action
        serializer_class = ReadOthelloUserSerializer

        if _action == 'create':
            serializer_class = CreateOthelloUserSerializer

        return serializer_class

    def get_permissions(self):
        _action = self.action
        permission_classes = self.permission_classes

        if _action == 'create':
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]
