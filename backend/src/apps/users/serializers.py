from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm password"
    )

    class Meta:
        model = CustomUser
        fields = (
            'phone_number', 'password', 'password2',
            'full_name', 'email', 'user_type',
            'farm_name', 'location', 'delivery_address'
        )

    def validate(self, attrs):
        """Check password match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_email(self, value):
        """
        Optional: enforce unique email if provided.
        Since model allows null/blank, we only check non‑blank emails.
        """
        if value:
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "A user with this email already exists."
                )
        return value

    def create(self, validated_data):
        # Remove password2 (not needed for user creation)
        validated_data.pop('password2')
        
        # Extract password and phone_number so they aren't in extra_fields
        password = validated_data.pop('password')
        phone_number = validated_data.pop('phone_number')
        
        # Remaining fields (full_name, email, user_type, etc.) go to extra_fields
        user = CustomUser.objects.create_user(
            phone_number=phone_number,
            password=password,
            **validated_data
        )
        return user