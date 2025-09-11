from django.urls import path, include
from .views import OrdersViewSet, OrderCountView, CompletedOrderCountView
from rest_framework import routers

"""URL configuration for Order-related API endpoints.

This module defines the routes for managing orders, including CRUD operations,
retrieving the total order count for a business user, and retrieving the count
of completed orders.
"""

router = routers.SimpleRouter()
router.register(r'orders', OrdersViewSet, basename="orders")

urlpatterns = [
    path('',  include(router.urls)),
    path('order-count/<int:business_user_id>/',
         OrderCountView.as_view(), name="order_count-detail"),
    path('completed-order-count/<int:business_user_id>/',
         CompletedOrderCountView.as_view(), name="completed_order_count-detail")
]
