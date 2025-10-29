from rest_framework import serializers
from django.contrib.auth.models import User
from profile_app.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles creation of new User instances along with associated UserProfile.
    Includes validation for email uniqueness and password confirmation.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        """
        Meta options for UserRegistrationSerializer.

        Specifies the User model and the fields included in serialization.
        """
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password']

    def validate(self, data):
        """
        Validate email uniqueness and password confirmation.

        Parameters:
            data: dict
                The input data provided for user registration.

        Returns:
            dict: The validated data if all checks pass.

        Raises:
            serializers.ValidationError: If email already exists or passwords do not match.
        """
        email = data.get('email')
        password = data.get('password')
        repeated_password = data.get('repeated_password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exist')

        if password != repeated_password:
            raise serializers.ValidationError('Passwords do not match')

        return data

    def save(self):
        """
        Create a new User and associated UserProfile.

        Automatically sets the password and assigns a user type (default 'customer').

        Returns:
            User: The newly created User instance.
        """
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']

        account = User(username=username, email=email)
        account.set_password(password)
        account.save()

        user_type = self.context.get('type', 'customer')
        UserProfile.objects.create(
            user=account,
            username=account.username,
            first_name=account.first_name,
            last_name=account.last_name,
            email=account.email,
            type=user_type
        )
        return account


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for general User data.

    Used to represent basic user information such as username, name, and email.
    """

    class Meta:
        """
        Meta options for UserSerializer.

        Specifies the User model and the fields included in serialization.
        """
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
