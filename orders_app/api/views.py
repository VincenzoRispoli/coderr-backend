
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .serializers import OrderSerializer
from rest_framework.response import Response
from orders_app.models import Order
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .permissions import IsCustomerUserForPostOrReadOnlyOrders, IsBusinessUserForUpdateOrder


class OrdersViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Order objects.

    Provides full CRUD operations on orders with custom permissions:
    - Customers can create orders and have read-only access.
    - Business users can update orders they are associated with.
    """

    serializer_class = OrderSerializer
    permission_classes = [
        IsCustomerUserForPostOrReadOnlyOrders, IsBusinessUserForUpdateOrder
    ]

    def get_queryset(self):
        """
        Return a queryset of Order objects filtered by the current user if provided.

        Supports filtering by 'creator_id' query parameter to return orders 
        where the current user is either the customer or business user.

        Returns:
            QuerySet: Filtered queryset of Order instances.
        """
        queryset = Order.objects.all()
        current_user = self.request.query_params.get('creator_id')
        if current_user:
            queryset = queryset.filter(
                Q(customer_user=current_user) | Q(business_user=current_user)
            )
        return queryset

    def perform_create(self, serializer):
        """
        Handle creation of a new Order instance.

        Delegates the creation to the serializer's save method, which 
        automatically handles assignment of customer and business users 
        as defined in the OrderSerializer.

        Parameters:
            serializer: OrderSerializer
                The serializer instance used to validate and save the new order.
        """
        serializer.save()


class OrderCountView(APIView):
    """
    API view to retrieve the total number of orders for a specific business user.

    Provides an endpoint to get the count of all orders associated with a given
    business user ID.
    """

    def get(self, request, business_user_id):
        """
        Handle GET requests.

        Retrieves the total number of orders where the specified user is the business user.

        Parameters:
            request: Request
                The HTTP request object.
            business_user_id: int
                The ID of the business user whose orders are being counted.

        Returns:
            Response: JSON response containing 'order_count' and HTTP 200 OK status.
        """
        count = Order.objects.filter(business_user=business_user_id).count()
        return Response({'order_count': count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    API view to retrieve the number of completed orders for a specific business user.

    Provides an endpoint to get the count of all orders with status 'completed'
    associated with a given business user ID.
    """

    def get(self, request, business_user_id):
        """
        Handle GET requests.

        Retrieves the total number of completed orders where the specified user
        is the business user.

        Parameters:
            request: Request
                The HTTP request object.
            business_user_id: int
                The ID of the business user whose completed orders are being counted.

        Returns:
            Response: JSON response containing 'completed_order_count' and HTTP 200 OK status.
        """
        completed_order_count = Order.objects.filter(
            business_user=business_user_id, status="completed"
        ).count()
        return Response(
            {'completed_order_count': completed_order_count},
            status=status.HTTP_200_OK
        )
