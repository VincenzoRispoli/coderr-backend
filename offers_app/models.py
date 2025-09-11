from django.db import models
from django.contrib.auth.models import User
from profile_app.models import UserProfile

# Create your models here.


class Offer(models.Model):
    """
    Represents an offer created by a user profile.

    Attributes:
        user (UserProfile): The owner of the offer. If the user is deleted, all their offers are deleted.
        title (str): The title of the offer (max length 100). Optional.
        file (FileField): An optional file associated with the offer, stored in 'offer-images/'.
        description (str): A detailed description of the offer (max length 1000).
        created_at (date): The date when the offer was created. Set automatically.
        updated_at (date): The date when the offer was last updated. Set automatically.
        min_price (Decimal): The minimum price for the offer.
        min_delivery_time (int): Minimum delivery time in days. Defaults to 1.
    """

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    file = models.FileField(blank=True, null=True, upload_to='offer-images/')
    description = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    min_price = models.DecimalField(max_digits=100, decimal_places=2)
    min_delivery_time = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'


class OfferDetails(models.Model):

    """
    Represents the details of a specific offer.

    Attributes:
        offer (Offer): The related offer. Deleting the offer deletes all related details.
        title (str): Title for the specific offer detail (max length 255).
        revisions (int): Number of revisions included in this offer detail.
        delivery_time_in_days (int): Delivery time in days for this detail option.
        price (Decimal): Price for this offer detail.
        offer_type (str): Type or category of this offer detail (max length 100).
    """

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    offer_type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Offer Detail'


class Features(models.Model):
    """
    Represents an individual feature associated with an offer detail.

    Attributes:
        offer_details (OfferDetails): The related offer detail. Deleting it deletes the features.
        name (str): The name of the feature (max length 255).
    """
    
    offer_details = models.ForeignKey(
        OfferDetails, on_delete=models.CASCADE, related_name="features")
    name = models.CharField(max_length=255)
