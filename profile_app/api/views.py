
from .serializers import UserProfileSerializer, BusinessUserProfileSerializer,  CustomerUserProfileSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics
from profile_app.models import UserProfile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerForPatchDeleteOrReadOnlyProfiles


class BusinessProfilesListView(APIView):
    """
    API view to retrieve all business user profiles.

    Provides an endpoint to return a list of UserProfile instances 
    where the type is 'business'.
    """

    def get(self, request):
        """
        Handle GET requests.

        Retrieves all UserProfile records of type 'business' and returns them 
        serialized.

        Parameters:
            request: Request
                The HTTP request object.

        Returns:
            Response: JSON response containing serialized business profiles
                      and HTTP 200 OK status.
        """
        user_profiles = UserProfile.objects.filter(type="business")
        serializer = BusinessUserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfilesListView(APIView):
    """
    API view to retrieve all customer user profiles.

    Provides an endpoint to return a list of UserProfile instances 
    where the type is 'customer'.
    """

    def get(self, request):
        """
        Handle GET requests.

        Retrieves all UserProfile records of type 'customer' and returns them 
        serialized.

        Parameters:
            request: Request
                The HTTP request object.

        Returns:
            Response: JSON response containing serialized customer profiles
                      and HTTP 200 OK status.
        """
        user_profiles = UserProfile.objects.filter(type="customer")
        serializer = CustomerUserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update a single user profile.

    Allows authenticated users to retrieve or update their own UserProfile.
    Permissions enforce that only the owner can modify the profile, 
    while read-only access is allowed otherwise.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerForPatchDeleteOrReadOnlyProfiles
    ]
    lookup_field = 'user'
