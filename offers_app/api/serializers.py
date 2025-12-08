
from offers_app.models import Offer, OfferDetails
from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import UserProfile


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

    class Meta:
        model = OfferDetails
        fields = [
            'id', 'title', 'offer', 'revisions',
            'delivery_time_in_days', 'price', 'offer_type', 'features'
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model.

    This serializer includes nested details and user-related information.
    It provides methods to handle creation and updating of Offer objects 
    along with their related OfferDetails entries.
    """

    user_details = serializers.SerializerMethodField()
    details = OfferDetailSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    min_price = serializers.DecimalField(
        max_digits=100, decimal_places=2, coerce_to_string=False, read_only=True)

    class Meta:
        """
        Meta configuration for the OfferSerializer.

        Specifies the model associated with the serializer and the 
        fields to be included in the serialized representation.
        """
        model = Offer
        fields = [
            'id', 'user', 'user_details', 'details',
            'title', 'image', 'description', 'created_at',
            'updated_at', 'min_price', 'min_delivery_time'
        ]

    def get_user_details(self, obj):
        """
        Retrieve basic user information related to the offer.

        Parameters:
            obj: Offer instance being serialized.

        Returns:
            dict: Dictionary containing the user's first name, last name, and username.
        """
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def create(self, validated_data):
        """
        Create a new Offer instance along with its related OfferDetails.

        Parameters:
            validated_data: Dictionary of validated input data.

        Returns:
            Offer: The created Offer instance.
        """
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        prices = []
        delivery_times = []

        # Create each related OfferDetails entry
        for detail_data in details_data:
            detail = OfferDetails.objects.create(offer=offer, **detail_data)
            prices.append(detail.price)
            delivery_times.append(detail.delivery_time_in_days)
            offer.min_price = min(prices) if prices else 0
            offer.min_delivery_time = min(delivery_times) if prices else 0
        return offer

    def update(self, instance, validated_data):
        """
        Update an existing Offer instance and its related OfferDetails.

        Parameters:
            instance: The existing Offer object to update.
            validated_data: Dictionary of validated input data.

        Returns:
            Offer: The updated Offer instance.
        """
        offer_details_data = validated_data.pop('details', {})
        self.save_offer_instance(instance, validated_data)

        # Update each related OfferDetails entry
        details = instance.details.all()
        for detail_instance, offer_detail_data in zip(details, offer_details_data):
            self.save_details_instance(detail_instance, offer_detail_data)

        return instance

    def save_offer_instance(self, instance, validated_data):
        """
        Update the given Offer instance with validated data.

           Iterates over each key-value pair in the validated data and assigns 
        the value to the corresponding attribute of the Offer instance. 
        The instance is saved after updating each attribute.

        Parameters:
            instance: Offer
            The Offer instance to update.
            validated_data: dict
            Dictionary containing the validated data for the offer.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()

    def save_details_instance(self, detail_instance, offer_detail_data):
        """
        Update a related OfferDetails instance using the OfferDetailSerializer.

        Initializes a serializer with the existing OfferDetails instance 
        and the provided data (partial update allowed). If the data is valid, 
        the serializer saves the updated instance.

        Parameters:
            detail_instance: OfferDetails
                The OfferDetails instance to update.
            offer_detail_data: dict
                Dictionary containing the validated data for the offer detail.
        """
        offer_detail_serializer = OfferDetailSerializer(
            detail_instance, data=offer_detail_data, partial=True)
        if offer_detail_serializer.is_valid():
            offer_detail_serializer.save()
