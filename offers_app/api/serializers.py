
from offers_app.models import Offer, OfferDetails, Features
from rest_framework import serializers
from django.contrib.auth.models import User

from profile_app.models import UserProfile


class FeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Features model.

    This serializer handles the representation of individual features
    associated with an OfferDetail. The `offer_details` field is read-only
    and represents the related offer detail instance.

    Attributes:
        offer_details (PrimaryKeyRelatedField): Read-only reference to the
            related OfferDetail instance.
        name (str): The name of the feature.

    Meta:
        model (Features): The model associated with this serializer.
        fields (list): List of fields to include in serialization.
    """
    offer_details = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Features
        fields = ['id', 'offer_details', 'name']


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferDetails model.

    This serializer represents detailed options for an offer, including
    nested features associated with each detail. The `offer` field is
    read-only and links back to the parent Offer.

    Attributes:
        offer (PrimaryKeyRelatedField): Read-only reference to the related
            Offer instance.
        features (FeatureSerializer): Nested serializer for associated
            features. Supports multiple entries.

    Meta:
        model (OfferDetails): The model associated with this serializer.
        fields (list): List of fields to include in serialization.
    """
    offer = serializers.PrimaryKeyRelatedField(read_only=True)
    features = FeatureSerializer(many=True)

    class Meta:
        model = OfferDetails
        fields = [
            'id', 'title', 'offer', 'revisions',
            'delivery_time_in_days', 'price', 'offer_type', 'features'
        ]


class OfferDetailHyperLinkSerializer(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for the OfferDetails model.

    This serializer provides a minimal representation of OfferDetails
    with a hyperlink to the detailed view. Useful for nested or list
    representations where only the URL reference is required.

    Meta:
        model (OfferDetails): The model associated with this serializer.
        fields (list): List of fields to include in serialization.
        extra_kwargs (dict): Additional configuration for the URL field,
            including the view name and lookup field.
    """

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offerdetails-detail', 'lookup_field': 'pk'}
        }


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model.

    This serializer handles the representation, creation, and updating of
    Offer objects along with their related OfferDetails and Features.
    It includes custom logic for nested relationships and provides
    additional computed fields such as `user_details`.

    Attributes:
        user_details (SerializerMethodField): Provides read-only details
            about the related user (first name, last name, username).
        details (OfferDetailSerializer): Nested serializer for offer
            details, supporting multiple entries.
        user (PrimaryKeyRelatedField): Read-only primary key reference to
            the related UserProfile.
        user_id (PrimaryKeyRelatedField): Write-only field to set the
            related UserProfile when creating an offer.

    Meta:
        model (Offer): The model associated with this serializer.
        fields (list): List of fields to be included in serialization
            and deserialization.
    """
    user_details = serializers.SerializerMethodField()
    details = OfferDetailSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        write_only=True,
        source='user'
    )

    class Meta:
        model = Offer
        fields = ['id', 'user', 'user_id', 'user_details', 'details',
                  'title', 'file', 'description', 'created_at',
                  'updated_at', 'min_price', 'min_delivery_time']

    def get_user_details(self, obj):
        """
        Return basic details of the user associated with the offer.

        Args:
            obj (Offer): The offer instance being serialized.

        Returns:
            dict: A dictionary containing the user's first name,
            last name, and username.
        """
        return {
            "first_name": obj.user.user.first_name,
            "last_name": obj.user.user.last_name,
            "username": obj.user.user.username
        }

    def create(self, validated_data):
        """
        Create a new Offer instance along with its nested details and
        features.

        Args:
            validated_data (dict): The validated input data.

        Returns:
            Offer: The created offer instance.
        """
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features_data = detail_data.pop('features', [])
            detail = OfferDetails.objects.create(offer=offer, **detail_data)
            for feature_data in features_data:
                Features.objects.create(offer_details=detail, **feature_data)
        return offer

    def update(self, instance, validated_data):
        """
        Update an existing Offer instance along with its nested details
        and features.

        Args:
            instance (Offer): The offer instance to update.
            validated_data (dict): The validated input data.

        Returns:
            Offer: The updated offer instance.
        """
        offer_details_data = validated_data.pop('details', {})
        self.save_offer_instance(instance, validated_data)

        details = instance.details.all()
        for detail_instance, offer_detail_data in zip(details, offer_details_data):
            features_data = offer_detail_data.pop('features', [])
            self.save_details_instance(detail_instance, offer_detail_data)

            features = detail_instance.features.all()
            for feature_intance, feature_data in zip(features, features_data):
                self.save_features_instance(feature_intance, feature_data)

        return instance

    def save_offer_instance(self, instance, validated_data):
        """
        Save the attributes of an offer instance.

        Args:
            instance (Offer): The offer instance to update.
            validated_data (dict): The validated attributes and values.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()

    def save_details_instance(self, detail_instance, offer_detail_data):
        """
        Save or update an offer detail instance using its serializer.

        Args:
            detail_instance (OfferDetails): The detail instance to update.
            offer_detail_data (dict): The validated attributes for the detail.
        """
        offer_detail_serializer = OfferDetailSerializer(
            detail_instance, data=offer_detail_data, partial=True)
        if offer_detail_serializer.is_valid():
            offer_detail_serializer.save()

    def save_features_instance(self, feature_intance, feature_data):
        """
        Save or update a feature instance using its serializer.

        Args:
            feature_intance (Features): The feature instance to update.
            feature_data (dict): The validated attributes for the feature.
        """
        feature_serializer = FeatureSerializer(
            feature_intance, data=feature_data, partial=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
