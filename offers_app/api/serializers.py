from offers_app.models import Offer, OfferDetails
from rest_framework import serializers


class OfferDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetails model.
    Handles validation and serialization of offer detail data.
    """
    price = serializers.FloatField()

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = OfferDetails
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

    def validate_title(self, value):
        """
        Validate that the offer title is at least 3 characters long.
        """
        if value is None or len(value) < 3:
            raise serializers.ValidationError(
                "Der Titel der Angebotsdetails muss mindestens 3 Zeichen lang sein"
            )
        return value

    def validate_price(self, value):
        """
        Validate that the price is greater than zero.
        """
        if value is None or value <= 0:
            raise serializers.ValidationError(
                "Der Preis muss größer als 0 sein"
            )
        return value

    def validate_delivery_time_in_days(self, value):
        """
        Validate that the delivery time is at least 1 day.
        """
        if value is None or value <= 0:
            raise serializers.ValidationError(
                "Die Lieferzeit in Tagen muss mindestens 1 betragen"
            )
        return value


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer model.
    Handles nested serialization and persistence of related offer details.
    """
    details = OfferDetailsSerializer(many=True)

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def validate_title(self, value):
        """
        Validate that the offer title is at least 3 characters long.
        """
        if value is None or len(value) < 3:
            raise serializers.ValidationError(
                "Der Titel des Angebots muss mindestens 3 Zeichen lang sein"
            )
        return value

    def create(self, validated_data):
        """
        Create an Offer instance along with its related OfferDetails.
        """
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)

        for detail in details_data:
            OfferDetails.objects.create(offer=offer, **detail)

        return offer

    def update(self, instance, validated_data):
        """
        Update an Offer instance and partially update its related OfferDetails.
        """
        details_data = validated_data.pop('details', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        details = instance.details.all()
        for detail_instance, single_detail_data in zip(details, details_data):
            offer_detail_serializer = OfferDetailsSerializer(
                detail_instance,
                data=single_detail_data,
                partial=True,
            )
            if offer_detail_serializer.is_valid():
                offer_detail_serializer.save()

        return instance


class OfferUrlSerializer(serializers.ModelSerializer):
    """
    Serializer that exposes a minimal representation of OfferDetails,
    including a dynamically generated detail URL.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = OfferDetails
        fields = ["id", "url"]

    def get_url(self, obj):
        """
        Build and return the URL for the offer details resource.
        """
        return f"/offerdetails/{obj.id}/"


class OfferHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for OfferDetails.
    Provides a URL-based representation of the resource.
    """

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = OfferDetails
        fields = ["id", "url"]


class OfferListSerializer(OfferSerializer):
    """
    Serializer for listing offers.
    Extends OfferSerializer with aggregated data and user information.
    """
    user_details = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferUrlSerializer(many=True)
    min_price = serializers.FloatField(read_only=True)

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_user_details(self, obj):
        """
        Return basic public information about the offer owner.
        """
        user = obj.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferRetrieveSerializer(OfferSerializer):
    """
    Serializer for retrieving a single Offer instance.
    Uses hyperlinked representation for related OfferDetails.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferHyperLinkedSerializer(many=True)
    min_price = serializers.FloatField(read_only=True)

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]
