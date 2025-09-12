
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from profile_app.models import UserProfile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerForPatchDeleteOrReadOnlyProfiles


class BusinessProfilesListView(APIView):
    """API view for listing business user profiles."""

    def get(self, request):
        """Return a list of all profiles with type 'business'."""
        user_profiles = UserProfile.objects.filter(type="business")
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfilesListView(APIView):
    """API view for listing customer user profiles."""

    def get(self, request):
        """Return a list of all profiles with type 'customer'."""
        user_profiles = UserProfile.objects.filter(type="customer")
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ViewSet):
    """ViewSet for managing UserProfile instances.

    Supports listing all profiles, retrieving a single profile,
    and partially updating profile data, including related User fields.
    """

    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated,
                         IsOwnerForPatchDeleteOrReadOnlyProfiles]

    def list(self, request):
        """Return a list of all user profiles."""
        serializer = UserProfileSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """Return a single user profile by primary key."""
        user_profile = get_object_or_404(self.queryset, pk=pk)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        """Partially update a user profile and its related User data."""
        user_profile_data = self.get_destructured_user_object(request)
        user_profile = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, user_profile)
        serializer = UserProfileSerializer(
            user_profile, data=user_profile_data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_destructured_user_object(self, request):
        """Prepare and return a structured dictionary of UserProfile and User data."""
        destructured_user_object = self.destructure_user_object(request)
        username = request.data.get('user[username]')
        if username:
            destructured_user_object['user']['username'] = username
        return destructured_user_object

    def destructure_user_object(self, request):
        """Extract and structure nested User and UserProfile data from the request."""
        return {
            'user': {
                'first_name': request.data.get('user[first_name]'),
                'last_name': request.data.get('user[last_name]'),
                'email': request.data.get('user[email]'),
            },
            'tel': request.data.get('tel', ""),
            'location': request.data.get('location', ""),
            'description': request.data.get('description', ""),
            'working_hours': request.data.get('working_hours', ""),
            'file': request.data.get('file')
        }
