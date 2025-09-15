from django.urls import path, include
from .views import BusinessProfilesListView, CustomerProfilesListView, ProfileViewSet
from rest_framework import routers

"""URL configuration for UserProfile-related API endpoints.

This module defines routes for managing user profiles, including the standard
CRUD operations via a viewset, and custom endpoints for listing business and
customer profiles separately.
"""

router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('profiles/business/', BusinessProfilesListView.as_view()),
    path('profiles/customer/', CustomerProfilesListView.as_view()),
]
