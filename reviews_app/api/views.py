from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from profile_app.models import UserProfile
from django.contrib.auth.models import User
from reviews_app.models import Review
from .serializers import ReviewsListCreateSerializer, ReviewRetrieveUpdateDestroySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters, generics, permissions
from .permissions import IsCustomerUserForPostReviewsOrReadOnly, IsReviewOwnerForPatchDelete


class ReviewsView(generics.ListCreateAPIView):
    """
    API view for listing and creating Review instances.

    Provides endpoints to:
    - List reviews with optional filtering by business user or reviewer.
    - Create new reviews by authenticated customer users.
    """
    serializer_class = ReviewsListCreateSerializer
    permission_classes = [IsCustomerUserForPostReviewsOrReadOnly,permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    lookup_field = "pk"

    def get_queryset(self):
        """
        Return a queryset of Review instances filtered by query parameters.

        Supports filtering by:
        - business_user_id: Returns reviews associated with a specific business user.
        - reviewer_id: Returns reviews created by a specific reviewer.

        Returns:
            QuerySet: Filtered queryset of Review instances.
        """
        queryset = Review.objects.all()
        business_user_param = self.request.query_params.get('business_user_id')
        reviewer_param = self.request.query_params.get('reviewer_id')

        if business_user_param:
            queryset = queryset.filter(business_user=business_user_param)

        if reviewer_param:
            queryset = queryset.filter(reviewer=reviewer_param)

        return queryset

    
    def perform_create(self, serializer):
        reviewer = self.request.user
        serializer.save(reviewer=reviewer)


class ReviewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a single Review instance.

    Permissions enforce that only the review owner can modify or delete the review,
    while read-only access is allowed otherwise.
    """
    serializer_class = ReviewRetrieveUpdateDestroySerializer
    permission_classes = [IsReviewOwnerForPatchDelete]
    queryset = Review.objects.all()
    lookup_field = "pk"
