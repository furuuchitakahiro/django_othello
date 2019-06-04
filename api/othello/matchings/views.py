from rest_framework import viewsets, mixins
from matchings.models import Matching
from matchings.serializers import (
    ReadMatchingSerializer,
    CreateMatchingSerializer,
    UpdateMatchingSerializer,
    ReadMatchingListSerializer,
)


class MatchingViewSets(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """マッチング API

    """

    lookup_field = 'slug'
    queryset = Matching.objects.all()

    def get_serializer_class(self):
        _action = self.action
        serializer_class = ReadMatchingSerializer

        if _action == 'list':
            serializer_class = ReadMatchingListSerializer
        elif _action == 'create':
            serializer_class = CreateMatchingSerializer
        elif _action in ['update', 'partial_update']:
            serializer_class = UpdateMatchingSerializer

        return serializer_class
