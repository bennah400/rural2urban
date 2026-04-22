from rest_framework import permissions

class IsProducer(permissions.BasePermission):
    """
    Allow access only to users with user_type = 'producer'.
    """
    message = "You must be a registered producer to perform this action."

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'user_type', None) == 'producer'
        )

class IsConsumer(permissions.BasePermission):
    """
    Allow access only to users with user_type = 'consumer'.
    """
    message = "This action is restricted to consumers only."

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'user_type', None) == 'consumer'
        )

class IsProducerOrReadOnly(permissions.BasePermission):
    """
    Producers can create, update, delete; others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return IsProducer().has_permission(request, view)