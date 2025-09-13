
from rest_framework import status
from rest_framework.views import APIView
from offers_app.models import Offer
from profile_app.models import UserProfile
from reviews_app.models import Review
from django.db.models import Avg
from rest_framework.response import Response


class BaseInfoView(APIView):
    """API view to provide aggregated platform statistics.

    Returns counts of business profiles, reviews, offers, and the average
    review rating across the platform.
    """

    def get(self, request):
        """Handle GET requests to return platform statistics.

        Returns:
            Response: JSON response containing:
                - business_profile_count: Total number of business profiles.
                - review_count: Total number of reviews.
                - average_rating: Average rating of all reviews.
                - offer_count: Total number of offers.
        """
        business_profile_count = UserProfile.objects.filter(
            type="business"
        ).count()
        review_count = Review.objects.all().count() or 0
        average_rating = Review.objects.aggregate(
            Avg('rating'))['rating__avg'] or 0
        rounded_average_rating = round(average_rating, 1)
        offer_count = Offer.objects.all().count() or 0
        return Response({
            'business_profile_count': business_profile_count,
            'review_count': review_count,
            'average_rating': rounded_average_rating,
            'offer_count': offer_count
        }, status=status.HTTP_200_OK)
