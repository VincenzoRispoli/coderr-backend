from profile_app.models import UserProfile
from user_auth_app.api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model.

    Serializes UserProfile instances along with nested User data.
    Supports updating both the UserProfile fields and the related User
    object in a single request.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Meta options for the UserProfileSerializer."""

        model = UserProfile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'email', 'file', 'location', 'tel',
            'description', 'working_hours', 'type', 'created_at'
        ]


class BusinessUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'tel', 'description', 'working_hours', 'type']


class CustomerUserProfileSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'uploaded_at', 'type']
