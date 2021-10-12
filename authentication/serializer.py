from rest_framework import serializers
from customer.models import User
from customer.views import get_permissions_wit_login
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import json


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=10)
    password = serializers.CharField(max_length=20, min_length=5, write_only=True)
    tokens = serializers.CharField(max_length=100, min_length=50, read_only=True)
    user_permissions = serializers.CharField(max_length=100, min_length=50, read_only=True)
    user = serializers.CharField(max_length=100, min_length=50, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'tokens',
            'user_permissions',
            'user',
        )

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)
        user_permissions = get_permissions_wit_login(user.id)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")

        role = user.role.name
        return {'email': email, 'tokens': user.tokens, "user_permissions": user_permissions, 'user': user.id, 'role': role}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    error_message = {
        'bad_token': ('Token is required or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)