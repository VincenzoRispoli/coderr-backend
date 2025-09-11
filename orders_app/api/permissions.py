from rest_framework.permissions import SAFE_METHODS, BasePermission
from profile_app.models import UserProfile

class IsCustomerUserForPostOrReadOnlyOrders(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method == 'POST':
            customer_profile = user_profile and user_profile.type == 'customer'
            return request.user.is_authenticated and customer_profile

        return request.user.is_authenticated


class IsBusinessUserForUpdateOrder(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return True

        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            return False

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            business_user = user_profile and user_profile.type == "business"
            is_owner_of_the_order = user_profile.id == obj.business_user.id
            return request.user.is_authenticated and is_owner_of_the_order and business_user

        return False