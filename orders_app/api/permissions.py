from rest_framework.permissions import SAFE_METHODS, BasePermission
from profile_app.models import UserProfile


class IsCustomerUserForPostOrReadOnlyOrders(BasePermission):
    """
    Custom permission class for order-related operations.

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
                The HTTP request object containing method and user info.
            view: View
                The view being accessed.

        Returns:
            bool: True if the user is allowed to perform the request; 
                  otherwise, False.
        """
        # Allow safe (read-only) methods for all users
        if request.method in SAFE_METHODS:
            return True

        # Attempt to retrieve the user's profile
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            # Deny permission if the user has no associated profile
            return False

        # Allow POST requests only for authenticated users of type 'customer'
        if request.method == 'POST':
            customer_profile = user_profile and user_profile.type == 'customer'
            return request.user.is_authenticated and customer_profile

        # Allow other methods only if the user is authenticated
        return request.user.is_authenticated


class IsBusinessUserForUpdateOrder(BasePermission):
    """
    Custom permission class for managing order updates by business users.

    This permission allows:
    - Read-only access (SAFE_METHODS) for all users.
    - POST requests for all users.
    - PUT, PATCH, and DELETE requests only for authenticated users 
      who are of type 'business' and own the order.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine whether the requesting user has permission to perform 
        an action on a specific order object.

        Parameters:
            request: Request
                The HTTP request object.
            view: View
                The view being accessed.
            obj: Order
                The order instance being accessed.

        Returns:
            bool: True if the user has permission for the operation; otherwise, False.
        """
        # Allow safe (read-only) methods for all users
        if request.method in SAFE_METHODS:
            return True

        # Allow POST requests for all users
        if request.method == 'POST':
            return True

        # Attempt to retrieve the user's profile
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            # Deny permission if the user has no profile
            return False

        # Allow PUT, PATCH, and DELETE only for business users
        # who own the order and are authenticated
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            business_user = user_profile and user_profile.type == "business"
            is_owner_of_the_order = request.user == obj.business_user and business_user
            return request.user.is_authenticated and is_owner_of_the_order and business_user

        # Deny all other methods
        return False
