from rest_framework import permissions


class IsTurnPlayer(permissions.BasePermission):
    """ターンプレイヤーである

    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False

        if request.user != obj.turn_player:
            return False

        return True
