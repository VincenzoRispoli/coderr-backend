from django.contrib.auth.models import User
from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetails
from profile_app.models import UserProfile
from offers_app.api.serializers import OfferDetailsSerializer
from .functions import create_new_order


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing order data.

    Provides a read-only representation of orders, including
    pricing and related user information.
    """
    price = serializers.FloatField(read_only=True)

    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
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
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]


class OrderCreateSerializer(OrderListSerializer):
    """
    Serializer for creating new Order instances.
    Extends OrderListSerializer and adds validation for duplicate orders.
    """
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetails.objects.all(),
        write_only=True,
        source="offer_detail"
    )

    class Meta(OrderListSerializer.Meta):
        """
        Metadata configuration for the serializer.
        """
        model = Order
        fields = [
            "id",
            "offer_detail_id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        """
        Ensure that the customer has not already ordered the same offer.
        """
        request = self.context.get('request')
        customer_user = request.user if request else None
        attrs['customer_user'] = customer_user
        offer_detail = attrs.get('offer_detail')
        if Order.objects.filter(customer_user=customer_user, offer_detail=offer_detail).exists():
            raise serializers.ValidationError(
                {"detail": "Du hast dieses Produkt schon bestellt"})

        return attrs

    def create(self, validated_data):
        """
        Create a new Order instance based on the selected offer detail.
        Automatically assigns customer, business user, and copies offer info.
        """
        offer_detail = validated_data.get('offer_detail')
        new_order = create_new_order(offer_detail, validated_data)
        return new_order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Order instances.
    Inherits all fields from OrderListSerializer and allows updating status.
    """
    class Meta:
        """
        Metadata configuration for the serializer.
        """
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
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

    def validate_status(self, status):
        allowed_status = {'in_progress', 'cancelled', 'completed'}
        if not status:
            raise serializers.ValidationError(
                {"status": "Status ist erforderlich"})
        if not status in allowed_status:
            raise serializers.ValidationError(
                {"status": "Zulässige Werte sind: in_progress, cancelled or completed"})

        return status
