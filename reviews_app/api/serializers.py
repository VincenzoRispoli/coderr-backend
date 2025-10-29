from django.contrib.auth.models import User
from reviews_app.models import Review
from profile_app.models import UserProfile
from rest_framework import serializers
from profile_app.api.serializers import UserProfileSerializer


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Handles serialization and deserialization of Review instances,
    including read-only reviewer assignment and writable business user assignment.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta options for the ReviewsSerializer.

        Specifies the model and fields included in serialization.
        """
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
