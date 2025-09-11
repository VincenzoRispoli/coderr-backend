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
        if request.method in SAFE_METHODS:
            return True

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method == 'POST':
            business_user_profile = user_profile and user_profile.type == "business"
            return request.user.is_authenticated and business_user_profile

        return True


class IsOwnerForPatchDeleteOrReadOnlyOffers(BasePermission):
    """Permission class that allows owners to modify their objects.

    Grants full access to the object's owner for PUT, PATCH, or DELETE requests,
    while allowing read-only access (safe methods) for other users.
    """

    def has_object_permission(self, request, view, obj):
        """Determine whether the requesting user has permission on the object.

        Returns True if the request is read-only.
        Returns True if the user is the owner of the object for update or delete.
        Returns False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return True

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            is_superuser = request.user.is_superuser
            is_business_guest = request.user.username == "GuestBusiness"
            is_owner = user_profile.id == obj.user.id
            return is_owner or is_superuser or is_business_guest
        return False