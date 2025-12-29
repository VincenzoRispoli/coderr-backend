from django.contrib.auth.models import User
from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetails
from profile_app.models import UserProfile
from offers_app.api.serializers import OfferDetailsSerializer


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model used in listing orders.
    All fields are read-only except for those explicitly settable elsewhere.
    """
    price = serializers.FloatField(read_only=True)

    class Meta:
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
            "updated_at",
        ]
        read_only_fields = (
            "customer_user",
            "business_user",
            "offer_detail",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        )


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
        offer_detail = attrs.get('offer_detail')
        if Order.objects.filter(customer_user=customer_user, offer_detail=offer_detail).exists():
            raise serializers.ValidationError(
                "You have already ordered this product"
            )

        return attrs

    def create(self, validated_data):
        """
        Create a new Order instance based on the selected offer detail.
        Automatically assigns customer, business user, and copies offer info.
        """
        offer_detail = validated_data.get('offer_detail')
        return Order.objects.create(
            business_user=offer_detail.offer.user,
            customer_user=validated_data['customer_user'],
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )


class OrderUpdateSerializer(OrderListSerializer):
    """
    Serializer for updating Order instances.
    Inherits all fields from OrderListSerializer and allows updating status.
    """
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
            "updated_at",
        ]
