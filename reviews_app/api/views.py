from reviews_app.models import Review
from .serializers import ReviewCreateSerializer, ReviewListSerializer, ReviewRetrieveUpdateDestroySerializer
from rest_framework import filters, generics, permissions
from .permissions import IsCustomerUserForPostReviewsOrReadOnly, IsReviewOwnerForPatchDelete
from .functions import filter_reviews_queryset_with_business_user_param, filter_reviews_queryset_with_reviewer_param


class ReviewsView(generics.ListCreateAPIView):
    """
    API view for listing and creating Review instances.

    Provides endpoints to:
    - List reviews with optional filtering by business user or reviewer.
    - Create new reviews by authenticated customer users.
    """
    permission_classes = [permissions.IsAuthenticated,
                          IsCustomerUserForPostReviewsOrReadOnly]
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
            queryset = filter_reviews_queryset_with_business_user_param(
                queryset, business_user_param)

        if reviewer_param:
            queryset = filter_reviews_queryset_with_reviewer_param(
                queryset, reviewer_param)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        if self.request.method in ["GET", "PUT", "PATCH", "DELETE"]:
            return ReviewRetrieveUpdateDestroySerializer
        return ReviewListSerializer

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
