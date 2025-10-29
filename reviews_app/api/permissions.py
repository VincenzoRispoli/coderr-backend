from rest_framework.permissions import BasePermission, SAFE_METHODS
from profile_app.models import UserProfile


class IsCustomerUserForPostReviewsOrReadOnly(BasePermission):
    """
    Custom permission class for managing review creation and read-only access.

    This permission allows:
    - Read-only access (SAFE_METHODS) for all users.
    - POST requests only for authenticated users with a 'customer' profile type.
    """

    def has_permission(self, request, view):
        """
        Determine whether the requesting user has general permission 
        to perform the given action.

        Parameters:
            request: Request
                The HTTP request object.
            view: View
                The view being accessed.

        Returns:
            bool: True if the user is allowed to perform the request; otherwise, False.
        """
        # Allow safe (read-only) methods for all users
        if request.method in SAFE_METHODS:
            return True

        # Attempt to retrieve the user's profile
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            # Deny permission if the user has no profile
            return False

        # Allow POST requests only for authenticated users of type 'customer'
        if request.method == 'POST':
            print("Is ihm user profile?", user_profile)
            is_customer = user_profile and user_profile.type == "customer"
            return request.user.is_authenticated and is_customer


class IsReviewOwnerForPatchDelete(BasePermission):
    """
    Custom permission class for managing updates and deletion of reviews.

    This permission allows:
    - Read-only access (SAFE_METHODS) for all users.
    - PUT, PATCH, DELETE requests only for authenticated users of type 'customer'
      who are the owners of the review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine whether the requesting user has permission to perform 
        an action on a specific review object.

        Parameters:
            request: Request
                The HTTP request object.
            view: View
                The view being accessed.
            obj: Review
                The review instance being accessed.

        Returns:
            bool: True if the user has permission for the operation; otherwise, False.
        """
        # Allow safe (read-only) methods for all users
        if request.method in SAFE_METHODS:
            return True

        # Attempt to retrieve the user's profile
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            # Deny permission if the user has no profile
            return False

        # Allow PUT, PATCH, DELETE only for customers who own the review
        if request.method in ["PUT", "PATCH", "DELETE"]:
            is_customer = user_profile and user_profile.type == "customer"
            is_review_owner = obj.reviewer == request.user
            return is_customer and is_review_owner
