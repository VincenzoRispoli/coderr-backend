
from django.urls import path, include
from .views import RegistrationView, CustomLoginView

"""URL configuration for user authentication endpoints.

This module defines routes for user registration and login.
"""

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', CustomLoginView.as_view())
]
