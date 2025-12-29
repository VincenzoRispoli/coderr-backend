from rest_framework.views import APIView
from offers_app.models import Offer, OfferDetails
from .serializers import OfferSerializer, OfferDetailsSerializer, OfferListSerializer, OfferRetrieveSerializer
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from rest_framework import status, permissions
from .pagination import OfferPagination
from .permissions import IsBusinessUserOrReadOnlyOffers, IsOwnerForPatchDeleteOrReadOnlyOffers


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Offer instances.
    Supports CRUD operations with filtering, searching, ordering, and pagination.
    """

    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    ordering = ['-updated_at']
    permission_classes = [
        IsBusinessUserOrReadOnlyOffers,
        IsOwnerForPatchDeleteOrReadOnlyOffers,
        permissions.IsAuthenticated,
    ]
    lookup_field = 'id'

    def get_queryset(self):
        """
        Return filtered queryset based on optional query parameters:
        - creator_id: filter offers by user ID
        - max_delivery_time: filter offers with min_delivery_time <= given value
        """
        queryset = Offer.objects.all()
        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user=creator_id)

        min_delivery_time = self.request.query_params.get('max_delivery_time')
        if min_delivery_time:
            queryset = queryset.filter(
                min_delivery_time__lte=min_delivery_time
            )

        return queryset

    def perform_create(self, serializer):
        """
        Handle creation of an Offer instance.
        Calculates and sets min_price and min_delivery_time from nested details.
        Associates the current user as the offer creator.
        """
        user = self.request.user
        details = self.request.data['details']
        min_price = min(detail['price'] for detail in details)
        min_delivery_time = min(
            detail['delivery_time_in_days'] for detail in details
        )
        serializer.save(
            user=user,
            min_price=min_price,
            min_delivery_time=min_delivery_time
        )

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action:
        - list -> OfferListSerializer
        - retrieve -> OfferRetrieveSerializer
        - create/update/partial_update -> OfferSerializer
        """
        if self.action == "list":
            return OfferListSerializer
        if self.action == "retrieve":
            return OfferRetrieveSerializer
        return OfferSerializer


class OfferDetailListView(generics.ListCreateAPIView):
    """
    API view to list all OfferDetails or create a new one.
    Requires authenticated user.
    """
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]


class OffersDetailsSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single OfferDetails instance.
    Requires authenticated user.
    """
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]


class OfferOfBusinessUserView(APIView):
    """
    API view for retrieving offers belonging to a specific business user.

    Provides an endpoint to fetch offers associated with a given business user ID.
    If the user exists and is of type "business", their offer is returned.
    Otherwise, a message indicating that the customer user has no offers is returned.
    """

    def get(self, request, business_user_id):
        """
        Handle GET requests.

        Retrieve offers created by a specific business user, identified by their ID.
        If the user type is "business", return their offer data.

        Parameters:
            request: Request
                The HTTP request object.
            business_user_id: int
                The ID of the business user whose offers are requested.

        Returns:
            Response:
                - On success: JSON response containing the offer data and HTTP 200 OK.
                - If no business offers exist: JSON message indicating absence of offers.
        """
        offers = Offer.objects.filter(user=business_user_id)
        for offer in offers:
            if offer.user.type == "business":
                serializer = OfferSerializer(offer)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "The customer user do not have offers"})
