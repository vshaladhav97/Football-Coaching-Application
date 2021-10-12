from os import read
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Customer, Payment, User, Student, CustomerDocuments, Role
from master.models import AgeGroup, Ages
from master.serializer import AgeGroupSerializer
from course.models import CourseGroupData, CourseDetail

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'role_status',
            'permissions',
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=60, min_length=12, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'avatar', 'email', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'avatar')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'landline',
            'town',
            'address',
            'postal_code',
            'country_code',
            'profile_image',
        )


class CustomerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = (
            'user',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'landline',
            'address',
            'postal_code',
            'profile_image',
        )


class CustomerUserRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
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


class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
        )

    # def validate(self, attrs):
    #     password = attrs.get('password', '')
    #     print(password))
    #     if len(password) < 12:
    #         raise serializers.ValidationError(
    #             "The password should be of 12 characters"
    #         )
    #     return attrs


class StudentSerializer(serializers.ModelSerializer):
    age_group = AgeGroupSerializer(read_only=True)

    class Meta:
        model = Student
        fields = (
            'id',
            'first_name',
            'last_name',
            'age',
            'age_group',
            'school_name',
            'address_details',
        )


class UserDataTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = (
            'id',
            'first_name',
            'last_name',
            'town',
            'postal_code',
            'address',
            'profile_image',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = "Active"
        return data


class StudentDataTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'id',
            'first_name',
            'last_name',
            'age',
            'school_name',
        )


class CustomerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDocuments
        fields = (
            'file_path',
        )


class StudentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Student
        fields = ("id", "first_name", "last_name", "birthdate",
                  "ages", "medical_issue", "customer",)

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ages
        fields = ("id", "age",)


class CourseDetailWithCourseTypeSerializer(serializers.ModelSerializer):
    course_type = serializers.ReadOnlyField(
        source='course_type.course_name')
    class Meta:
        model = CourseDetail
        fields = ("id", "course_type",)

class CourseGroupDataForStudentSerializer(serializers.ModelSerializer):
    location = serializers.ReadOnlyField(
        source='course_detail.location.location')
    course_detail = CourseDetailWithCourseTypeSerializer(read_only = True)


    class Meta:
        model = CourseGroupData
        fields = ("id", "age", "start_time", "end_time", "location", "course_detail",)



class StudentGroupDataSerializer(serializers.ModelSerializer):
    ages = CourseGroupDataForStudentSerializer(read_only = True)
    class Meta:

        model = Student
        fields = ("id", "ages",)


class CustomerRegistrationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customer
        exclude = ['town', 'profile_image', 'deleted', ]


class CustomerIdForBookingSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customer
        fields = (
            "id",
            "first_name",
            "user",
        )


class ChildEditSerialier(serializers.ModelSerializer):

    class Meta:

        model = Student
        fields = ("id", "first_name", "last_name",
                  "medical_issue", "birthdate",)


class ChildEditSerialierData(serializers.ModelSerializer):
    class Meta:

        model = Student
        fields = ("id", "first_name", "last_name", "birthdate", "medical_issue",)
        # fields = ("id", "first_name", )



class ChildGetPrepopulateSerialierData(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(
        source='customer.first_name')
    address_detail_1 = serializers.ReadOnlyField(
        source='address_details.address_line_1')
    class Meta:

        model = Student
        fields = ("id", "first_name", "last_name", "school_name", "address_details_id","address_detail_1", "customer_name", "customer", "birthdate", "medical_issue",)


class CustomerIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ("id", "email", "user",)


class StudentDetailsByCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "first_name", "last_name", "customer", "ages",)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        # profile_data = validated_data.pop('profile')
        # user = User.objects.create(**validated_data)
        payment = Payment.objects.create(**validated_data)
        # payment.save()
        return payment

    def update(self, instance, validated_data):
        # print(validated_data)
        instance.Payment_gateway_reference_id = validated_data.get(
            'Payment_gateway_reference_id', instance.Payment_gateway_reference_id)
        instance.status = validated_data.get(
            'status', instance.status)
        instance.Payment_gateway_response_text = validated_data.get(
            'Payment_gateway_response_text', instance.Payment_gateway_response_text)
        instance.save()
        return instance
