from rest_framework import permissions
from .models import User

class RoleBasedPermission(permissions.BasePermission):
    """
    Permissions:
    - Admin: full access.
    - Vet: manage animals, vaccinations, reminders (no user management).
    - Receptionist: view animals and create/list reminders (treated as appointments).
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role == User.Role.ADMIN:
            return True

        if user.role == User.Role.VET:
            # Deny access to user management
            if getattr(view, "basename", None) == "users" or view.__class__.__name__ == "UserViewSet":
                return False
            return True

        if user.role == User.Role.RECEPTIONIST:
            view_name = view.__class__.__name__
            if view_name == "AnimalViewSet":
                return request.method in permissions.SAFE_METHODS
            if view_name == "ReminderViewSet":
                if request.method in ("POST", "GET", "HEAD", "OPTIONS"):
                    return True
                return False
            return False

        return False

    def has_object_permission(self, request, view, obj):
        # For now use same rules as has_permission.
        return self.has_permission(request, view)
