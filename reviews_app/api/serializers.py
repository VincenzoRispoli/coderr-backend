from reviews_app.models import Review
from profile_app.models import UserProfile
from rest_framework import serializers
from profile_app.api.serializers import UserProfileSerializer


class ReviewsSerializer(serializers.ModelSerializer):
    """Serializer for the Review model.

    Handles serialization and deserialization of Review instances,
    linking a business user and a reviewer via primary key fields.
    Includes rating, description, and timestamps.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(type="business")
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all()
    )

    class Meta:
        """Meta options for the ReviewsSerializer."""

        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at'
        ]
