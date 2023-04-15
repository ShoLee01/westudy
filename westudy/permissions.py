from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import University, User
from django.contrib.auth import get_user_model

class RegisterWithoutAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST' or request.method == 'GET' and not request.user.is_authenticated

class IsAdminUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, University):
            raise PermissionDenied({"message": "This endpoint is not available"})
        elif not isinstance(user, get_user_model()):
            raise PermissionDenied({"message": "Unauthenticated user"})
        elif not user.is_superuser:
            raise PermissionDenied({"message": "You do not have sufficient permissions"})
        
        return True
    

class IsUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, University):
            raise PermissionDenied({"message": "This endpoint is not available"})
        elif not request.user.is_authenticated:
            raise PermissionDenied({"message": "Unauthenticated user"})
        return True

    
class IsUniversityAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, University) and user.is_active:
            return True
        elif isinstance(user, University) and not user.is_active:
            raise PermissionDenied({"message": "This university is not active"})
        elif not isinstance(user, get_user_model()):
            raise PermissionDenied({"message": "This endpoint is not available"})
        elif not user.is_authenticated:
            raise PermissionDenied({"message": "Unauthenticated user"})
        elif not user.is_superuser:
            raise PermissionDenied({"message": "You do not have sufficient permissions"})
        return True
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        elif isinstance(user, User) and user.is_superuser:
            return True
        elif isinstance(user, University) and obj == user:
            return True
        return False




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