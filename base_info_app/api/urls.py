from django.urls import path, include
from .views import BaseInfoView

"""URL configuration for platform base information endpoint.

Provides a route to retrieve aggregated statistics such as counts of
business profiles, reviews, offers, and the average review rating.
"""

urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name="base-info")
]
