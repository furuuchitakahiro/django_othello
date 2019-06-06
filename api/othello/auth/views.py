from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from othello_users.serialiers import ReadOthelloUserSerializer
from auth.serializers import LoginSerializer, LogoutSerializer


class AuthViewSets(viewsets.GenericViewSet):
    """Auth API

    """

    def get_serializer_class(self):
        _action = self.action
        serializer_class = ReadOthelloUserSerializer

        if _action == 'login':
            serializer_class = LoginSerializer
        elif _action == 'logout':
            serializer_class = LogoutSerializer
        elif _action == 'me':
            serializer_class = ReadOthelloUserSerializer

        return serializer_class

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny]
    )
    def login(self, request):
        """ログイン API

        """
        # リクエスト内容をバリデーション
        validation_serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        validation_serializer.is_valid(raise_exception=True)

        user: 'othello_users.models.OthelloUser' = authenticate(
            request=request,
            email=request.data.get('email', ''),
            password=request.data.get('password', '')
        )
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _login(request, user)

        serializer = self.get_serializer(user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
    )
    def logout(self, request):
        """ログアウト API

        """
        _logout(request)
        serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['get'],
    )
    def me(self, request):
        """me API

        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
