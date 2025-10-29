from django.contrib.auth.models import User
from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetails
from profile_app.models import UserProfile
from offers_app.api.serializers import OfferDetailSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Handles serialization and deserialization of Order instances,
    including nested offer detail information. Automatically assigns
    customer and business users during creation.
    """

    offer_detail = OfferDetailSerializer(read_only=True)
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetails.objects.all(),
        write_only=True,
        source="offer_detail"
    )
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    revisions = serializers.IntegerField(read_only=True)
    delivery_time_in_days = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(read_only=True)
    offer_type = serializers.CharField(read_only=True)
    status = serializers.CharField(default="in_progress")
    created_at = serializers.DateField(read_only=True)
    updated_at = serializers.DateField(read_only=True)

    class Meta:
        """
        Meta configuration for the OrderSerializer.

        Specifies the model and fields included in serialization.
        """
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "offer_detail",
            "offer_detail_id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Create a new Order instance from validated data.

        Automatically assigns:
        - The authenticated user as the customer_user.
        - The corresponding business_user from the offer_detail.
        - Offer details such as title, revisions, delivery time, price, features, and type.

        Parameters:
            validated_data: dict
                Validated data from the serializer input.

        Returns:
            Order: The newly created Order instance.
        """
        request = self.context['request']
        offer_detail = validated_data.pop('offer_detail')
        return Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
