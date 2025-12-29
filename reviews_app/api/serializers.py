from django.contrib.auth.models import User
from reviews_app.models import Review
from profile_app.models import UserProfile
from rest_framework import serializers
from profile_app.api.serializers import UserProfileSerializer


class ReviewsListCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing Review instances.

    Handles:
    - Automatic assignment of the reviewer (read-only)
    - Writable assignment of the business_user
    - Validation to prevent duplicate reviews by the same reviewer for the same business
    """
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta configuration for the serializer.
        """
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        """
        Ensure that a reviewer cannot create multiple reviews for the same business user.

        Raises:
            serializers.ValidationError: If a review by the same reviewer already exists.
        """
        request = self.context['request']
        reviewer = request.user
        business_user = data.get('business_user')

        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError(
                "Du hast diesen Geschäftnutzer shon bewertet"
            )

        return data


class ReviewRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving, updating, or deleting a Review instance.
    Validates that a rating and description are provided for updates.
    """

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        """
        Ensure that both rating and description are present when updating a review.

        Raises:
            serializers.ValidationError: If rating or description is missing.
        """
        rating = data.get('rating')
        description = data.get('description')
        errors = []

        if not rating:
            errors.append(
                "Eine Rezension kann nicht ohne Sternebewertung aktualisiert werden."
            )

        if not description:
            errors.append(
                "Eine Rezension kann nicht ohne Beschreibung aktualisiert werden."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return data
