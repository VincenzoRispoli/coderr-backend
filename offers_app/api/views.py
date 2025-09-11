from django.shortcuts import get_object_or_404
from profile_app.models import UserProfile
from .permissions import IsOwnerForPatchDeleteOrReadOnlyOffers, IsBusinessUserOrReadOnlyOffers
from .serializers import OfferDetailSerializer, OfferSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from offers_app.models import Offer, OfferDetails, Features
from .throttling import OfferThrottle, OfferGetThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters, permissions
from .pagination import OfferPagination


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing offers.

    Provides list, retrieve, create, update, and delete actions.
    Supports filtering by creator_id and max_delivery_time,
    as well as search, ordering, and pagination.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [
        IsOwnerForPatchDeleteOrReadOnlyOffers, IsBusinessUserOrReadOnlyOffers]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['min_price', 'updated_at']
    ordering = ['-updated_at']
    pagination_class = OfferPagination

    def get_queryset(self):
        """
        Optionally filter offers by creator_id or max_delivery_time.

        Returns:
            QuerySet: Filtered list of offers.
        """
        offer_user_id = self.request.query_params.get('creator_id')
        if offer_user_id:
            self.queryset = self.queryset.filter(user=offer_user_id)

        min_delivery_time_param = self.request.query_params.get(
            'max_delivery_time')
        if min_delivery_time_param:
            self.queryset = self.queryset.filter(
                min_delivery_time__lte=min_delivery_time_param
            )

        return self.queryset


class OfferDetailsView(APIView):
    """
    API view for listing and creating offer details.

    Methods:
        get(request): Retrieve all offer details.
        post(request): Create a new offer detail.
    """

    def get(self, request):
        """Return a list of all offer details."""
        offer_details = OfferDetails.objects.all()
        serializer = OfferDetailSerializer(offer_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new offer detail."""
        serializer = OfferDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OffersDetailsSingleView(APIView):
    """
    API view for retrieving and updating a single offer detail.

    Methods:
        get(request, pk): Retrieve a single offer detail by its ID.
        put(request, pk): Update an existing offer detail by its ID.
    """

    def get(self, request, pk):
        """Return a single offer detail by its primary key."""
        offer_detail = OfferDetails.objects.get(pk=pk)
        serializer = OfferDetailSerializer(
            offer_detail, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update an offer detail by its primary key."""
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
    API view for retrieving offers of a specific business user.

    Methods:
        get(request, business_user_id): Retrieve offers belonging to a business user.
    """

    def get(self, request, business_user_id):
        """Return offers of a business user if available."""
        offers = Offer.objects.filter(user=business_user_id)
        for offer in offers:
            if offer.user.type == "business":
                serializer = OfferSerializer(offer)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "The customer user do not have offers"})
