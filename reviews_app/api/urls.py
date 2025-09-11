from django.urls import path, include
from rest_framework import routers
from .views import ReviewsViewSet

"""URL configuration for Review-related API endpoints.

This module defines routes for managing reviews, including CRUD operations
via the ReviewsViewSet.
"""

router = routers.SimpleRouter()
router.register(r'reviews', ReviewsViewSet, basename="reviews")

urlpatterns = [
    path('', include(router.urls)),
]
