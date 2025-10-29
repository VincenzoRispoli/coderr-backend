from django.urls import path, include
from .views import BusinessProfilesListView, CustomerProfilesListView, ProfileView
from rest_framework import routers

"""URL configuration for UserProfile-related API endpoints.

This module defines routes for managing user profiles, including the standard
CRUD operations via a viewset, and custom endpoints for listing business and
customer profiles separately.
"""

urlpatterns = [
    path('profile/<int:user>/', ProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfilesListView.as_view()),
    path('profiles/customer/', CustomerProfilesListView.as_view()),
]
