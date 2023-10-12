from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Доступ автора привычки"""
    message = "У вас недостаточно прав для выполнения данного действия"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by:
            return True
        return False


class IsPublic(BasePermission):
    """Доступ к публичным привычкам"""
    message = "У вас недостаточно прав для выполнения данного действия"

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return False
