from django.db.models import fields
from rest_framework import serializers
from .models import (Company, AddressDetail, Location, AgeGroup, Months, PlayingSurface,
                     CourseType, EventType, WeekDay, ClassStatus, Ages)


class AddressDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressDetail
        fields = (
            'id',
            'address_line_1',
            'address_line_2',
            'address_line_3',
            'town',
            'country',
        )

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'id',
            'company_name',

        )

class LocationSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Location
        fields = (
            'id',
            'location',
            'company',
            'address_line_1',
            'address_line_1',
            'address_line_2',
            'address_line_3',
            'town',
            'country',
            'postal_code'
        )

class LocationForAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'location',
 
        )



class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'id',
            'company_name',

        )


class LocationDataTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = (
             'id',
             'company',
             'location',
             'address_line_1',
             'town',
             'postal_code',
             'playing_surface', 
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        company = Company.objects.get(pk=data['company'])
        data['company'] = company.company_name
        # playing_surface = PlayingSurface.objects.get(pk=data['playing_surface'])
        # data['playing_surface'] = playing_surface.surface
        return data

class LocationDataTableSerializerForPrepolated(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = (
             'id',
             'company',
             'location',
             'address_line_1',
             'town',
             'postal_code',
             'playing_surface',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        company = Company.objects.get(pk=data['company'])
        data['company'] = company.company_name
        playing_surface = PlayingSurface.objects.get(pk=data['playing_surface'])
        data['playing_surface'] = playing_surface.surface
        data['playing_surface_id'] = playing_surface.id
        return data


class AgeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = (
            'id',
            'age_group_text',
        )


class CourseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseType
        fields = (
            'id',
            'course_name',
            'course_description',
            'course_title',
        )



class EvenTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = (
            'id',
            'type_name',
        )


class WeekDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WeekDay
        fields = (
            'id',
            'weekday',
        )


class ClassStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassStatus
        fields = (
            'id',
            'status_name',
        )


class MonthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Months
        fields = (
            'id',
            'month',
        )


class AgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ages
        fields = (
            'id',
            'age',
        )


class PlayingSurfaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayingSurface
        fields = (
            'id',
            'surface',
        )


class CompanyNameDropdownSelectionSerializer(serializers.ModelSerializer):
    """Company Name serializer for dropdown"""
    class Meta:
        model = Company
        fields = ("id", "company_name",)