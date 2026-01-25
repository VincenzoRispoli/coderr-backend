from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from profile_app.models import UserProfile
from reviews_app.models import Review


class IsCustomerUserForPostReviewsOrReadOnly(BasePermission):
    """
    Allow read-only access to all users.
    Allow POST only if the user has a 'customer' UserProfile.
    """

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            raise PermissionDenied("Der Benutzer besitzt kein Benutzerprofil.")

        if request.method == "POST":
            if user_profile.type != "customer":
                raise PermissionDenied(
                    "Nur Benutzer mit Kundenprofil dürfen Bewertungen erstellen."
                )
            return True


class IsReviewOwnerForPatchDelete(BasePermission):
    """
    Custom permission for updating or deleting reviews.

    Allows:
    - Read-only access for all users.
    - PUT, PATCH, DELETE only for authenticated customers who own the review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user has permission to modify a review object.

        Args:
            request: The HTTP request.
            view: The view being accessed.
            obj: The Review instance.

        Returns:
            bool: True if user is allowed, False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method in ["PUT", "PATCH", "DELETE"]:
            is_customer = user_profile.type == "customer"
            is_review_owner = obj.reviewer == request.user
            return is_customer and is_review_owner
