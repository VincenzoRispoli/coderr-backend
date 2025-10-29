from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Min, Max
from profile_app.models import UserProfile
from .permissions import IsOwnerForPatchDeleteOrReadOnlyOffers, IsBusinessUserOrReadOnlyOffers
from .serializers import OfferDetailSerializer, OfferSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from offers_app.models import Offer, OfferDetails
from rest_framework import filters
from .pagination import OfferPagination


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Offer objects.

    Provides full CRUD functionality for offers, including search,
    ordering, pagination, and custom filtering by creator and delivery time.
    Custom permissions ensure that only authorized users can modify offers.
    """

    serializer_class = OfferSerializer
    permission_classes = [
        IsOwnerForPatchDeleteOrReadOnlyOffers, IsBusinessUserOrReadOnlyOffers
    ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['min_price', 'updated_at']
    ordering = ['-updated_at']
    pagination_class = OfferPagination

    def get_queryset(self):
        """
        Return a queryset of Offer objects filtered by query parameters.

        Supports filtering by:
        - creator_id: filters offers by the user who created them.
        - max_delivery_time: filters offers with delivery time less than or equal to the provided value.

        Returns:
            QuerySet: Filtered queryset of Offer instances.
        """
        queryset = Offer.objects.all()
        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user=creator_id)

        min_delivery_time_param = self.request.query_params.get(
            'max_delivery_time')
        if min_delivery_time_param:
            queryset = queryset.filter(
                min_delivery_time__lte=min_delivery_time_param
            )

        return queryset

    def perform_create(self, serializer):
        """
        Handle creation of a new Offer instance.

        Automatically assigns:
        - The authenticated user as the offer creator.
        - The minimum price across all provided details.
        - The minimum delivery time among all details.

        Parameters:
            serializer: OfferSerializer
                The serializer instance used to validate and save the new offer.
        """
        offer_user = User.objects.get(id=self.request.user.id)
        details = self.request.data['details']

        # Calculate minimum price and minimum delivery time from offer details
        min_price = min(detail['price'] for detail in details)
        min_delivery_time = min(
            detail['delivery_time_in_days'] for detail in details)

        # Save the new offer with computed and user-related data
        serializer.save(
            user=offer_user,
            min_price=min_price,
            min_delivery_time=min_delivery_time
        )


class OfferDetailsView(APIView):
    """
    API view for managing OfferDetails objects.

    Provides endpoints to:
    - Retrieve a list of all offer details (GET).
    - Create a new offer detail (POST).
    """

    def get(self, request):
        """
        Handle GET requests.

        Retrieves and returns all OfferDetails records in the system.

        Parameters:
            request: Request
                The HTTP request object.

        Returns:
            Response: JSON response containing a list of serialized offer details
                      and HTTP 200 OK status.
        """
        offer_details = OfferDetails.objects.all()
        serializer = OfferDetailSerializer(offer_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST requests.

        Creates a new OfferDetails record based on the provided request data.

        Parameters:
            request: Request
                The HTTP request object containing the offer detail data.

        Returns:
            Response: 
                - On success: JSON response with serialized data and HTTP 201 Created.
                - On failure: JSON response with validation errors and HTTP 400 Bad Request.
        """
        serializer = OfferDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OffersDetailsSingleView(APIView):
    """
    API view for retrieving and updating a single OfferDetails instance.

    Provides endpoints to:
    - Retrieve a specific offer detail by its primary key (GET).
    - Update a specific offer detail partially or fully (PUT).
    """

    def get(self, request, pk):
        """
        Handle GET requests.

        Retrieve and return a single OfferDetails object identified by its primary key.

        Parameters:
            request: Request
                The HTTP request object.
            pk: int
                Primary key of the OfferDetails instance to retrieve.

        Returns:
            Response: JSON response containing serialized offer detail data 
                      and HTTP 200 OK status.
        """
        offer_detail = OfferDetails.objects.get(pk=pk)
        serializer = OfferDetailSerializer(
            offer_detail, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Handle PUT requests.

        Update an existing OfferDetails instance with the provided data.
        The update is partial (fields can be updated individually).

        Parameters:
            request: Request
                The HTTP request object containing update data.
            pk: int
                Primary key of the OfferDetails instance to update.

        Returns:
            Response:
                - On success: JSON response with updated data and HTTP 202 Accepted.
                - On failure: JSON response with validation errors and HTTP 400 Bad Request.
        """
        offer_detail = OfferDetails.objects.get(pk=pk)
        serializer = OfferDetailSerializer(
            offer_detail, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
