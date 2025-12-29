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
    """
    Serializer for business user profiles.

    Inherits from ModelSerializer to automatically generate fields
    and validation rules based on the UserProfile model.

    The 'user' field is represented as a PrimaryKeyRelatedField, which
    uses the User model's primary key (ID). It is set as read-only,
    meaning it cannot be created or modified through this serializer.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta configuration for the BusinessUserProfileSerializer.

        - model: Specifies the model this serializer is based on.
        - fields: Lists the fields included in serialization and deserialization.
        """
        model = UserProfile
        fields = [
            'user', 'username', 'first_name',
            'last_name', 'file','location', 'tel', 'description',
            'working_hours', 'type'
        ]


class CustomerUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for customer user profiles.

    This serializer includes fewer fields than the business version,
    as customers typically do not require attributes such as phone
    number, description, or working hours.

    The 'user' field is a PrimaryKeyRelatedField set to read-only,
    ensuring that the associated User cannot be modified through
    this serializer.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta configuration for the CustomerUserProfileSerializer.

        - model: Specifies the model this serializer is based on.
        - fields: Defines which fields will be serialized or deserialized.
        """
        model = UserProfile
        fields = [
            'user', 'username', 'first_name',
            'last_name', 'file', 'type'
        ]
