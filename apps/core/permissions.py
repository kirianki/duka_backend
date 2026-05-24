from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allows access only to the Owner.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsShopOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a shop to edit it.
    Assumes the model instance has an `owner` attribute or a `shop.owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'shop'):
            return obj.shop.owner == request.user
        return False
