
from django.shortcuts import get_object_or_404
from django.db.models import Q
from profile_app.models import UserProfile
from django.contrib.auth.models import User
from .serializers import OrderListSerializer, OrderCreateSerializer, OrderUpdateSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders_app.models import Order
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .permissions import IsCustomerUserForPostOrReadOnlyOrders, IsBusinessUserForUpdateOrder


class OrdersViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Order instances.
    Supports CRUD operations with permissions based on user role.
    """
    permission_classes = [
        IsCustomerUserForPostOrReadOnlyOrders,
        IsBusinessUserForUpdateOrder,
        IsAuthenticated
    ]

    def get_queryset(self):
        """
        Return orders related to the current user, either as customer or business user.
        """
        queryset = Order.objects.all()
        current_user = self.request.user
        if current_user:
            queryset = queryset.filter(
                Q(customer_user=current_user) | Q(business_user=current_user)
            )
        return queryset

    def perform_create(self, serializer):
        """
        Save a new instance with any additional context or fields before committing to the database.

        In DRF, 'self.context["request"]' is automatically available in the serializer,
        so you can use it to associate the current user or other request-specific data.
        """
        serializer.save()

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action:
        - create -> OrderCreateSerializer
        - update/partial_update -> OrderUpdateSerializer
        - list/retrieve -> OrderListSerializer
        """
        if self.action == "create":
            return OrderCreateSerializer
        if self.action in ["update", "partial_update"]:
            print("Order update gerufen")
            return OrderUpdateSerializer
        return OrderListSerializer


class OrderCountView(APIView):
    """
    API view to return the total number of orders for a specific business user.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Retrieve and return the count of orders for the given business user ID.
        Validates that the user exists and is a business user.
        """
        try:
            user = UserProfile.objects.get(user_id=business_user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Der Benutzer existiert nicht"}, status=status.HTTP_404_NOT_FOUND
                            )

        if user.type != "business":
            return Response(
                {"detail": "Nur Geschäftsnutzer können ihre Bestellungen zählen."}, status=status.HTTP_403_FORBIDDEN
            )

        count = Order.objects.filter(
            business_user=business_user_id, status="in_progress").count()
        return Response({"order_count": int(count)}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    API view to return the total number of completed orders for a specific business user.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """
        Retrieve and return the count of completed orders for the given business user ID.
        Validates that the user exists and is a business user.
        """
        try:
            user = UserProfile.objects.get(user_id=business_user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Der Benutzer existiert nicht"}, status=status.HTTP_404_NOT_FOUND)

        if user.type != "business":
            return Response({"detail": "Nur Geschäftsnutzer können ihre Bestellungen zählen."}, status=status.HTTP_403_FORBIDDEN)

        completed_order_count = Order.objects.filter(
            business_user=business_user_id, status="completed"
        ).count()
        return Response(
            {'completed_order_count': completed_order_count},
            status=status.HTTP_200_OK
        )
