from profile_app.models import UserProfile
from user_auth_app.api.serializers import UserSerializer
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model.

    Serializes UserProfile instances along with nested User data.
    Supports updating both the UserProfile fields and the related User
    object in a single request.
    """

    user = UserSerializer()

    class Meta:
        """Meta options for the UserProfileSerializer."""

        model = UserProfile
        fields = [
            'user', 'id', 'file', 'location', 'tel',
            'description', 'working_hours', 'type', 'uploaded_at'
        ]
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
        }

    def update(self, instance, validated_data):
        """Update a UserProfile instance along with its related User object."""
        user_data = validated_data.pop('user', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        user = instance.user
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

        return instance
