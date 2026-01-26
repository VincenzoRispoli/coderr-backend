from rest_framework.permissions import BasePermission, SAFE_METHODS
from profile_app.models import UserProfile


class IsBusinessUserOrReadOnlyOffers(BasePermission):
    """
    Permission class to control access to Offer creation and read-only operations.

    Rules:
    - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for any user.
    - All other methods require the user to be authenticated.
    - POST requests are allowed only if the authenticated user has a related
      UserProfile of type "business".
    - Any other non-safe write requests are denied.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has permission to access the view
        based on the HTTP method and the user's profile.
        """

        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method == 'POST':
            business_user_profile = user_profile.type == "business"
            return business_user_profile

        return False


class IsOwnerForPatchDeleteOrReadOnlyOffers(BasePermission):
    """
    Object-level permission for Offer instances.

    - Requires the user to be authenticated.
    - PUT and PATCH requests are allowed only for the owner of the Offer.
    - DELETE requests are allowed for the owner or a superuser.
    - All other methods are denied at the object level.
    """

    def has_permission(self, request, view):
        """
        Allow access only to authenticated users.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Grant object-level access based on ownership and HTTP method.
        """

        is_superuser = request.user.is_superuser
        is_owner = request.user == obj.user

        if request.method in ('PUT', 'PATCH'):
            return is_owner

        if request.method == "DELETE":
            return is_owner or is_superuser

        return False
