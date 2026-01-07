from profile_app.api.serializers import UserProfileSerializer
from profile_app.models import UserProfile
from .serializers import UserRegistrationSerializer
from .functions import fill_user_data_dict, guest_user_data_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User


class RegistrationView(APIView):
    """API view to handle user registration, including guest users.

    Supports registration and login for normal users, guest customers, and
    guest businesses. Returns authentication token and user profile data.
    """

    def post(self, request):
        """Handle POST requests for user registration or guest login.

        Routes requests based on the username to guest customer/business
        handlers or normal registration.
        """
        serializer = UserRegistrationSerializer(
            data=request.data, context={'type': request.data['type']}
        )
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = fill_user_data_dict(token, saved_account)
        else:
            data = {
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


class CustomLoginView(ObtainAuthToken):
    """API view to handle user login and return authentication token."""

    def post(self, request):
        """Authenticate a user and return token and user profile data.

        Returns:
            Response: HTTP 200 with user data on success, or 400 with errors.
        """
        username = request.data.get('username')
        if username == 'GuestBusiness':
            return self.process_guest_business_reg_or_login(username, request)

        if username == 'GuestCustomer':
            return self.process_guest_customer_reg_or_login(username, request)

        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            data = fill_user_data_dict(token, user)
        else:
            data = {
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def register_user(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data, context={'type': request.data['type']})
        if serializer.is_valid():
            saved_account = serializer.save()
            token, _ = Token.objects.get_or_create(user=saved_account)
            data = fill_user_data_dict(token, saved_account)
        else:
            data = {
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)
    

    def process_guest_customer_reg_or_login(self, username, request):
        """Handle registration or login for a guest customer user."""
        try:
            data = self.get_guest_customer_user_data(username)
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return self.register_user(request)
    

    def process_guest_business_reg_or_login(self, username, request):
        """Handle registration or login for a guest business user."""
        try:
            data = self.get_guest_business_user_data(username)
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return self.register_user(request)

    def get_guest_customer_user_data(self, username):
        """Return data dict for an existing guest customer user."""
        guest_customer_user = User.objects.get(username=username)
        token, _ = Token.objects.get_or_create(user=guest_customer_user)
        data = guest_user_data_dict(
            token, guest_customer_user)
        return data
    

    def get_guest_business_user_data(self, username):
        """Return data dict for an existing guest business user."""
        guest_business_user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=guest_business_user)
        data = guest_user_data_dict(
            token, guest_business_user)
        return data
