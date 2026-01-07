from orders_app.models import Order

def create_new_order(offer_detail, validated_data):
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
