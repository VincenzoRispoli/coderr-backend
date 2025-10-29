from django.urls import path, include
from rest_framework import routers
from .views import ReviewsView, ReviewsDetailView

"""URL configuration for Review-related API endpoints.

This module defines routes for managing reviews, including CRUD operations
via the ReviewsViewSet.
"""

urlpatterns = [
    path('reviews/', ReviewsView.as_view(), name="reviews-list"),
    path('reviews/<int:pk>/', ReviewsDetailView.as_view(), name="reviews-detail")
]
