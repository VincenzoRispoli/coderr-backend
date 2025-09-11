from django.db import models
from profile_app.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Review(models.Model):
    """Model representing a review for a business user.

    Each Review links a reviewer (user) to a business user, stores a rating
    between 1 and 5, includes a description, and tracks creation and update
    timestamps.
    """

    business_user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="business_user_review"
    )
    reviewer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="reviewer"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.description
