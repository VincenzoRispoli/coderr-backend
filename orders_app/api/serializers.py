from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetails
from profile_app.models import UserProfile
from offers_app.api.serializers import OfferDetailSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model.

    This serializer manages the conversion of Order instances to and from 
    JSON representations. It handles relationships between customer and 
    business users, links an offer detail either by its ID or as a nested 
    read-only object, and includes metadata such as status and timestamps. 
    It ensures that data integrity is preserved by restricting related fields 
    to specific user types and validating offer references.
    """
    offer_detail = OfferDetailSerializer(read_only=True)
    customer_user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.filter(type="customer"))
    business_user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.filter(type="business"))
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset = OfferDetails.objects.all(),
        write_only = True,
        source="offer_detail"
    )
    
    
    
    class Meta:
        model = Order
        fields = ['id','customer_user', 'business_user','offer_detail_id', 'offer_detail', 'status', 'created_at', 'updated_at']