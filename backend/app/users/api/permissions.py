import copy
from rest_framework import permissions


class IsStaff(permissions.DjangoModelPermissions):

    # https://stackoverflow.com/questions/46584653/django-rest-framework-use-djangomodelpermissions-on-listapiview
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class UserProfilesPermissions(permissions.BasePermission):
    """
    Custom permissions for API routes interacting with user profiles (used in ViewSet)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action in ['destroy']:
            return obj == request.user or request.user.is_superuser
        else:
            return False


class UserProfilesUpdatePermissions(UserProfilesPermissions):
    """
    Custom permissions for API routes to updating user profiles (used in View)
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
