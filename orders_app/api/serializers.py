from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import NotFound
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
    offer_detail_id = serializers.IntegerField(
        write_only=True, required=False)

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
        Validate offer_detail_id: ensure it is provided, exists, 
        and not already ordered by the customer. 
        Adds 'offer_detail' and 'customer_user' to attrs.

        Raises:
            ValidationError: missing or duplicate order.
            NotFound: offer_detail does not exist.
        """
        request = self.context.get('request')
        customer_user = request.user if request else None
        offer_detail_id = attrs.get('offer_detail_id')
        if not offer_detail_id:
            raise serializers.ValidationError(
                {"offer_detail_id": "Die ID des Angebotsdetails ist für die erstellung einer Bestellung erförderlich"})

        try:
            offer_detail = OfferDetails.objects.get(pk=offer_detail_id)
        except OfferDetails.DoesNotExist:
            raise NotFound(
                {"offer_detail_id": "Der gesuchte Angebotsdetail existiert nicht"})

        if Order.objects.filter(customer_user=customer_user, offer_detail=offer_detail).exists():
            raise serializers.ValidationError(
                {"detail": "Du hast dieses Produkt bereits bestellt"})
        attrs['offer_detail'] = offer_detail
        attrs['customer_user'] = customer_user
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
