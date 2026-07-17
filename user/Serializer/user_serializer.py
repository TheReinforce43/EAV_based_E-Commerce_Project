from rest_framework import serializers 
from user.models import User 
from django.contrib.auth import authenticate
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.user_related import validate_bd_phone_number



from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'address', 'phone_number', 'profile_image', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                user_type=validated_data.get('user_type', 'customer'),
                address=validated_data.get('address', ''),
                phone_number=validated_data.get('phone_number', ''),
                profile_image=validated_data.get('profile_image', None)
            )
            return user

    def validate_phone_number(self, value):
        if not value:
            return value

        # 1. Format validation
        normalized = validate_bd_phone_number(value)  # raises ValidationError if invalid

        # 2. Uniqueness check
        if User.objects.filter(phone_number=normalized).exists():
            raise serializers.ValidationError("This phone number is already registered.")

        return normalized

    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({"detail": "Invalid email or password."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "This account is inactive."})

        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['user_type'] = user.user_type

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserSignUpSerializer(user, context=self.context).data
        }




class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError as e:
            print("TokenError:", str(e))   # check docker logs
            raise serializers.ValidationError({"detail": str(e)})  # temporarily show real error