from rest_framework.permissions import BasePermission

from account.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.kind == User.UserKind.ADMIN


class IsInspector(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.kind == User.UserKind.INSPECTOR


class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.kind == User.UserKind.SUPERVISOR
