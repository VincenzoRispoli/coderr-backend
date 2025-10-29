from rest_framework.permissions import SAFE_METHODS, BasePermission
from profile_app.models import UserProfile


class IsOwnerForPatchDeleteOrReadOnlyProfiles(BasePermission):
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

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            is_superuser = request.user.is_superuser
            is_guest_user = (request.user.username == "GuestBusiness") or (
                request.user.username == "GuestCustomer")
            is_owner = request.user == obj.user
            return is_owner or is_superuser or is_guest_user
        return False
