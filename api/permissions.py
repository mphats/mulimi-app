from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    def __init__(self, allowed):
        super().__init__()
        self.allowed = set(allowed)

    def has_permission(self, request, view):
        role = getattr(getattr(request.user, "profile", None), "role", None)
        return bool(request.user and request.user.is_authenticated and role in self.allowed)

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.seller == request.user or obj.author == request.user

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   getattr(getattr(request.user, "profile", None), "role", None) == "ADMIN")
