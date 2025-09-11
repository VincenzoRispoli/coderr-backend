from django.urls import path, include
from .views import BusinessProfilesListView, CustomerProfilesListView, ProfileViewSet
from rest_framework import routers

"""URL configuration for UserProfile-related API endpoints.

This module defines routes for managing user profiles, including the standard
CRUD operations via a viewset, and custom endpoints for listing business and
customer profiles separately.
"""

router = routers.SimpleRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/business/', BusinessProfilesListView.as_view()),
    path('profile/customer/', CustomerProfilesListView.as_view()),
]
