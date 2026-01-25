from django.contrib.auth.models import User
from reviews_app.models import Review
from profile_app.models import UserProfile
from rest_framework import serializers
from profile_app.api.serializers import UserProfileSerializer


class BaseReviewSerializer(serializers.ModelSerializer):
    """
    Base serializer for Review objects.

    Includes shared fields and prevents duplicate reviews
    by the same user for the same business user.
    """

    class Meta:
        """
        Serializer metadata for the Review model.
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
        Validate that a user can review a business user only once.

        Args:
            data: Validated serializer data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If a duplicate review exists.
        """
        reviewer = self.context['request'].user
        business_user = data.get('business_user')

        if business_user and Review.objects.filter(
            business_user=business_user,
            reviewer=reviewer
        ).exists():
            raise serializers.ValidationError(
                {"detail": "Du hast schon diese Geschäftnutzer bewertet"}
            )

        return data


class ReviewListSerializer(BaseReviewSerializer):
    """
    Serializer for listing Review objects.

    Overrides user-related fields to return primary keys.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all())


class ReviewCreateSerializer(BaseReviewSerializer):
    """
    Serializer for creating Review objects.

    Applies custom validation rules and assigns the reviewer
    from the authenticated request user.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, error_messages={
            "required": "Der Geschäftsnutzer ist erforderlich.",
            "null": "Der Geschäftsnutzer darf nicht leer sein.",
            "does_not_exist": "Dieser Geschäftsnutzer existiert nicht.",
            "incorrect_type": "Ungültiger Geschäftsnutzer."
        })
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        allow_null=False,
        error_messages={
            "required": "Die Bewertung ist erforderlich.",
            "null": "Die Bewertung darf nicht leer sein.",
            "invalid": "Die Bewertung muss eine Zahl sein.",
            "min_value": "Die Bewertung muss mindestens 1 Stern sein.",
            "max_value": "Die Bewertung darf höchstens 5 Sterne sein.",
        })
    description = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        max_length=500,
        error_messages={
            "null": "Die Becshreibung darf nicht leer sein.",
            "blank": "Die Becshreibung darf nicht leer sein.",
            "max_length": "Die Beschreibung darf höchstens 500 Zeichen enthalten."
        })

    def validate(self, attrs):
        """
        Prevent duplicate reviews by the same user
        for the same business user.
        """
        business_user = attrs.get('business_user')
        reviewer = self.context['request'].user
        if Review.objects.filter(
            business_user=business_user,
            reviewer=reviewer
        ).exists():
            raise serializers.ValidationError(
                {"detail": "Du hast diesen Geschäftsnutzer bereits bewertet"}
            )

        return attrs

    def create(self, validated_data):
        """
        Create a Review instance and assign the reviewer
        from the request context.
        """
        reviewer = self.context['request'].user
        validated_data['reviewer'] = reviewer
        return Review.objects.create(**validated_data)


class ReviewRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving, updating, or deleting a Review instance.
    Validates that a rating and description are provided for updates.
    """

    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        required=False,
        allow_null=False,
        error_messages={
            "null": "Die Bewertung darf nicht leer sein.",
            "invalid": "Die Bewertung muss eine Zahl sein.",
            "min_value": "Die Bewertung muss mindestens 1 Stern sein.",
            "max_value": "Die Bewertung darf höchstens 5 Sterne sein.",
        })
    description = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        max_length=500,
        error_messages={
            "null": "Die Becshreibung darf nicht leer sein.",
            "blank": "Die Becshreibung darf nicht leer sein.",
            "max_length": "Die Beschreibung darf höchstens 500 Zeichen enthalten."
        })

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
