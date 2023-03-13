from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class RegisterWithoutAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST' or request.method == 'GET' and not request.user.is_authenticated

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied({"message": "Unauthenticated user"})
        elif not request.user.is_superuser:
            raise PermissionDenied({"message": "You do not have sufficient permissions"})
        return True

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id 


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id