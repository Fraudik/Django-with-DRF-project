from django.conf import settings
from rest_framework import serializers
from .models import CustomUser
from .validators import validate_otp_format


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class UserAuthSerializer(serializers.ModelSerializer):
    """
    Serializer for user data with sensitive information for auth (password)
    """

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')


class UserRegisterSerializer(UserAuthSerializer):
    class Meta(UserAuthSerializer.Meta):
        extra_kwargs = {"password": {'write_only': True}}


class UserLoginSerializer(UserAuthSerializer):
    # explicitly declare the username so that it is not checked for uniqueness during validation
    email = serializers.EmailField(validators=[])


class OTPSerializer(serializers.Serializer):
    """
    Serializer for validating OTP before checking it in database
    """
    otp = serializers.CharField(validators=[validate_otp_format])

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
