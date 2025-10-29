from django.db import models
from offers_app.models import Offer, OfferDetails
from profile_app.models import UserProfile, User

# Create your models here.


class Order(models.Model):
    """Database model representing an order.

    The Order model links a customer and a business user through a specific
    offer detail. It also tracks the current status of the order along with
    creation and update timestamps.
    """
    offer_detail = models.ForeignKey(OfferDetails, on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_user")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_user")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=100, default="in_progress")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
