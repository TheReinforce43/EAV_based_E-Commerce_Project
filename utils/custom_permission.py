from rest_framework.permissions  import BasePermission, SAFE_METHODS 



class isAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only permissions are allowed for any request.
    """

    def has_permission(self, request, view):
        

        user = request.user 

        if not user and not user.is_authenticated:
            return False

        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Allow access only for admin users for other methods
        return request.user and request.user.is_superuser