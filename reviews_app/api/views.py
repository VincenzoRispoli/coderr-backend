from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from reviews_app.models import Review
from .serializers import ReviewsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from profile_app.api.permissions import IsCustomerUserForPostReviewsOrReadOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Review instances.

    Provides standard CRUD operations using the ReviewsSerializer.
    Supports filtering by business user ID and reviewer ID via query parameters,
    and allows ordering by `updated_at` or `rating`.
    """

    serializer_class = ReviewsSerializer
    permission_classes = [IsCustomerUserForPostReviewsOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']

    def get_queryset(self):
        """Return a queryset of Review objects filtered by optional query parameters.

        Filters can include:
        - `business_user_id`: return reviews for a specific business user
        - `reviewer_id`: return reviews made by a specific reviewer
        """
        queryset = Review.objects.all()
        business_user_reviews_param = self.request.query_params.get(
            'business_user_id')
        reviewer_params = self.request.query_params.get('reviewer_id')
        if business_user_reviews_param:
            queryset = queryset.filter(
                business_user=business_user_reviews_param)

        if reviewer_params:
            queryset = queryset.filter(reviewer=reviewer_params)

        return queryset
