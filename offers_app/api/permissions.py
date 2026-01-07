from rest_framework.permissions import SAFE_METHODS, BasePermission
from profile_app.models import UserProfile


class IsBusinessUserOrReadOnlyOffers(BasePermission):
    """Custom permission to allow only business users to create offers.

    Read-only methods (GET, HEAD, OPTIONS) are allowed for any user.
    For write operations:
        - The user must be authenticated.
        - The user must have a related UserProfile.
        - The UserProfile must be of type "business".
    """

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method == 'POST':
            business_user_profile = user_profile.type == "business"
            return business_user_profile

        return True


class IsOwnerForPatchDeleteOrReadOnlyOffers(BasePermission):
    """
    Custom permission class for Offers objects.

    This permission allows:
    - Read-only access (SAFE_METHODS) for all users.
    - POST requests for all users.
    - PUT, PATCH, and DELETE requests only if the user is:
        * The owner of the object,
        * A superuser, or
        * The special user with username "GuestBusiness".
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine if the requesting user has permission for a specific object.

        Parameters:
            request: The HTTP request object.
            view: The view that triggered this permission check.
            obj: The object being accessed.

        Returns:
            bool: True if permission is granted, otherwise False.
        """

        if not request.user.is_authenticated:
            return False


        is_superuser = request.user.is_superuser
        is_owner = request.user == obj.user

        # Allow PUT, PATCH, and DELETE only for the owner or superuser
        if request.method in ('PUT', 'PATCH'):
            return is_owner

        if request.method == "DELETE":
            return is_owner or is_superuser

        return False
