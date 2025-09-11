from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Model representing a user profile with extended information.

    Each UserProfile is linked one-to-one with a User and stores additional
    data such as profile image, location, contact details, description,
    working hours, user type (customer or business), and the timestamp of
    profile creation.
    """

    USER_TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profile-images/', blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=30, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, choices=USER_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        """Return the username associated with this profile."""
        return self.user.username
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['user']
