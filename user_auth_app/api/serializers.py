from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration.

    Handles the creation of a new User along with a related UserProfile.
    Ensures password confirmation matches and checks for email uniqueness.
    """

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        """Meta options for UserRegistrationSerializer."""
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password']

    def validate(self, data):
        """Validate email uniqueness and password confirmation."""
        email = data.get('email')
        password = data.get('password')
        repeated_password = data.get('repeated_password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exist')

        if password != repeated_password:
            raise serializers.ValidationError('Passwords do not match')

        return data

    def save(self):
        """Create a new User and associated UserProfile."""
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()

        user_type = self.context.get('type', 'customer')
        UserProfile.objects.create(user=account, type=user_type)
        return account


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model.

    Used to serialize and update User objects with optional fields.
    """

    class Meta:
        """Meta options for UserSerializer."""
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
