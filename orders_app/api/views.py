
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .serializers import OrderSerializer
from rest_framework.response import Response
from orders_app.models import Order
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .permissions import IsCustomerUserForPostOrReadOnlyOrders, IsBusinessUserForUpdateOrder


class OrdersViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Order instances.

    Provides CRUD operations for the Order model using the OrderSerializer.
    The queryset can be filtered by the `creator_id` query parameter, allowing
    retrieval of orders where the current user is either the customer or
    the business user.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsCustomerUserForPostOrReadOnlyOrders, IsBusinessUserForUpdateOrder]

    def get_queryset(self):
        """Return a queryset of Order objects filtered by the current user if provided."""
        queryset = Order.objects.all()
        current_user = self.request.query_params.get('creator_id')
        if current_user:
            queryset = queryset.filter(
                Q(customer_user=current_user) | Q(business_user=current_user))
        return queryset


class OrderCountView(APIView):
    """API view for retrieving the number of orders for a given business user."""

    def get(self, request, business_user_id):
        """Return the total count of orders for the specified business user."""
        count = Order.objects.filter(business_user=business_user_id).count()
        return Response({'order_count': count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """API view for retrieving the number of completed orders for a given business user."""

    def get(self, request, business_user_id):
        """Return the count of completed orders for the specified business user."""
        completed_order_count = Order.objects.filter(
            business_user=business_user_id, status="completed").count()
        return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)
