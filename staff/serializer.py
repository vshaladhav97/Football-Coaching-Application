from rest_framework import serializers
from .models import Staff
from customer.serializer import UserSerializer


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'landline',
            'address',
            'postal_code',
        )


class StaffUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = (
            'user',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'landline',
            'address',
            'postal_code',
        )


class StaffDataTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'id',
        )