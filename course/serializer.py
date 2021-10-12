from re import L
from django.core.serializers import serialize
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import (CourseDetail, CourseGroupData, CourseLocation, BookCourseDetail, CourseMonths, Message,
                     Events, Notification, UserAttendance, AccountRecordKeeping, Cart, CartItem, Coach, BookingCustomerStudentDetails, EventWeek,
                     DayWiseWeekDetails, Order, OrderSummary, PriceMatrix, NurseryAndWeeklyStudentOrderDetails)
from master.serializer import (AgeGroupSerializer, LocationSerializer, AddressDetailSerializer,
                               CourseTypeSerializer, EvenTypeSerializer, WeekDaySerializer,
                               ClassStatusSerializer, MonthSerializer, AgeSerializer, CompanySerializer)
from customer.serializer import StudentSerializer, UserDataSerializer
from master.models import CourseType, Location, AgeGroup, ClassStatus, Ages, Company
from customer.models import Student, User, Role, Customer
from customer.models import Student, User
from actstream.models import Action
from dateutil import parser
from datetime import datetime, timedelta, date
import json
import time
import math


class CourseMonthSerializer(serializers.ModelSerializer):
    month = MonthSerializer(read_only=True)

    class Meta:
        model = CourseMonths
        fields = (
            'month',
        )


class CourseListingDataSerializer(serializers.ModelSerializer):
    age_group = AgeGroupSerializer(read_only=True)
    course_type = CourseTypeSerializer(read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'id',
            'course_type',
            'course_description',
            'age_group',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course_description'] = data['course_description'][0:450]
        data['id'] = data['id']
        return data


# class CourseDetailSerializer(serializers.ModelSerializer):
#     # age_group = AgeGroupSerializer(read_only=True)
#     # event_type = EvenTypeSerializer(read_only=True)
#     location = LocationSerializer(read_only=True)
#     class_status = ClassStatusSerializer(read_only=True)
#     course_type = CourseTypeSerializer(read_only=True)
#     # course_months = CourseMonthSerializer(source="coursemonths_set", many=True, read_only=True)

#     class Meta:
#         model = CourseDetail
#         fields = (
#             'id',
#             'course_type',
#             'no_of_groups',
#             'no_of_weeks',
#             'default_course_rate',
#             'joining_fee',
#             'course_description',
#             'location',
#             # 'age_group',
#             'start_date',
#             'end_date',
#             'single_day',
#             'two_days',
#             'three_days',
#             'four_days',
#             'five_days',
#             'street',
#             'town',
#             'postal_code',
#             'playing_surface',
#             'coach',
#             'class_status',
#             'welcome_message',
#         )


# class CourseGroupDataSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = CourseGroupData
#         fields = (
#             'id',
#             'course_detail',
#             'age',
#             'from_drop_off_time',
#             'from_pick_up_time',
#             'to_drop_off_time',
#             'to_pick_up_time',
#             'start_time',
#             'end_time',
#             'maximum_capacity',
#             'coach1',
#             'coach2',
#         )

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['time'] = data['start_time']
#         if data['from_pick_up_time']:
#             data['time'] = data['from_pick_up_time']

#         if data['coach1']:
#             coach1 = Coach.objects.get(pk=data['coach1'])
#             data['coach1'] = coach1.first_name

#         if data['coach2']:
#             coach2 = Coach.objects.get(pk=data['coach2'])
#             data['coach2'] = coach2.first_name
#         return data
class tests_rotas(serializers.ModelSerializer):

    Model = CourseGroupData
    fields = ("__all__")

# class CourseGroupDataSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = CourseGroupData
#         fields = (
#             'id',
#             'course_detail',
#             'age',
#             'from_drop_off_time',
#             'from_pick_up_time',
#             'to_drop_off_time',
#             'to_pick_up_time',
#             'start_time',
#             'end_time',
#             'maximum_capacity',
#             'coach1',
#             'coach2',
#         )

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['time'] = data['start_time']
#         if data['from_pick_up_time']:
#             data['time'] = data['from_pick_up_time']

#         if data['coach1']:
#             coach1 = Coach.objects.get(pk=data['coach1'])
#             data['coach1'] = coach1.first_name

#         if data['coach2']:
#             coach2 = Coach.objects.get(pk=data['coach2'])
#             data['coach2'] = coach2.first_name
#         return data


class CourseGroupDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseGroupData
        fields = (
            'id',
            'course_detail',
            'age',
            'from_drop_off_time',
            'from_pick_up_time',
            'to_drop_off_time',
            'to_pick_up_time',
            'start_time',
            'end_time',
            'maximum_capacity',
            'coach1',
            'coach2',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['start_time']:

            data['time'] = data['start_time']
            print("", data['time'])
        if data['from_pick_up_time']:
            data['time'] = data['from_pick_up_time']

        if data['coach1']:
            coach1 = Coach.objects.get(pk=data['coach1'])
            data['coach1'] = coach1.first_name

        if data['coach2']:
            coach2 = Coach.objects.get(pk=data['coach2'])
            data['coach2'] = coach2.first_name
        return data


class CourseDetailSerializer1(serializers.ModelSerializer):
    # age_group = AgeGroupSerializer(read_only=True)
    # event_type = EvenTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class_status = ClassStatusSerializer(read_only=True)
    course_type = CourseTypeSerializer(read_only=True)
    # course_months = CourseMonthSerializer(source="coursemonths_set", many=True, read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'id',
            'course_type',
            'no_of_groups',
            'no_of_weeks',
            'default_course_rate',
            'joining_fee',
            'course_description',
            'location',
            # 'age_group',
            'start_date',
            'end_date',
            'single_day',
            'two_days',
            'three_days',
            'four_days',
            'five_days',
            'street',
            'town',
            'postal_code',
            'playing_surface',
            'coach',
            'class_status',
            'welcome_message',
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    # age_group = AgeGroupSerializer(read_only=True)
    # event_type = EvenTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class_status = ClassStatusSerializer(read_only=True)
    course_type = CourseTypeSerializer(read_only=True)
    course_details = CourseGroupDataSerializer(many=True,
                                               read_only=True)
    # course_months = CourseMonthSerializer(source="coursemonths_set", many=True, read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'id',
            'course_type',
            'no_of_groups',
            'no_of_weeks',
            'default_course_rate',
            'joining_fee',
            'course_description',
            'location',
            # 'age_group',
            'start_date',
            'end_date',
            'single_day',
            'two_days',
            'three_days',
            'four_days',
            'five_days',
            'street',
            'town',
            'postal_code',
            'playing_surface',
            'coach',
            'class_status',
            'welcome_message',
            'course_details',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data, "test")
        # b = {x['time']: x for x in data['course_group_data']}.values()
        # print("hello", data)
        if data['course_details']:
            # print("inside if")
            b = json.dumps(list(
                {x['time']: x for x in data['course_details'] if 'course_details' in data}.values()))

        # print(type(b), type(data['course_details']))
        # print(data['course_details'])
        # print(b)
        if data['course_details']:
            data['course_details'] = b
        return data


class CourseDetailSerializerForCourseCreation(serializers.ModelSerializer):
    # age_group = AgeGroupSerializer(read_only=True)
    # event_type = EvenTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class_status = ClassStatusSerializer(read_only=True)
    course_type = CourseTypeSerializer(read_only=True)
    course_group_data = CourseGroupDataSerializer(source='coursegroupdata_set', many=True,
                                                  read_only=True)
    # course_months = CourseMonthSerializer(source="coursemonths_set", many=True, read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'id',
            'course_type',
            'no_of_groups',
            'no_of_weeks',
            'default_course_rate',
            'joining_fee',
            'course_description',
            'location',
            # 'age_group',
            'start_date',
            'end_date',
            'single_day',
            'two_days',
            'three_days',
            'four_days',
            'five_days',
            'street',
            'town',
            'postal_code',
            'playing_surface',
            'coach',
            'class_status',
            'welcome_message',
            'course_group_data',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data, "test")
        # b = {x['time']: x for x in data['course_group_data']}.values()

        # b = json.dumps(list({x['time']: x for x in data['course_group_data'] if 'course_group_data' in data}.values()))

        # # print(type(b), type(data['course_group_data']))
        # # print(data['course_group_data'])
        # # print(b)
        # data['course_group_data'] = b
        return data


class CourseDetailDataSerializer(serializers.ModelSerializer):
    # age_group = AgeGroupSerializer(read_only=True)
    event_type = EvenTypeSerializer(read_only=True)

    location = LocationSerializer(read_only=True)
    class_status = ClassStatusSerializer(read_only=True)
    course_type = CourseTypeSerializer(read_only=True)
    # course_months = CourseMonthSerializer(source="coursemonths_set", many=True, read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'id',
            'course_type',
            'no_of_groups',
            'no_of_weeks',
            'default_course_rate',
            'joining_fee',
            'course_description',
            'location',
            'logo',
            'start_date',
            'end_date',
            'single_day',
            'two_days',
            'three_days',
            'four_days',
            'five_days',
            'street',
            'town',
            'postal_code',
            'playing_surface',
            'coach',
            'class_status',
            'event_type',
            'welcome_message',
        )


class CourseDataTableSerializer(serializers.ModelSerializer):
    course_type = CourseTypeSerializer(read_only=True)
    # class_status = ClassStatusSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'course_type',
            'class_status',
            'course_description',
            'start_date',
            'end_date',
            'location',
            'default_course_rate',
            'id',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data)
        course_type = CourseType.objects.get(pk=data['course_type']['id'])
        data['course_type'] = course_type.course_name
        data['course_type_id'] = course_type.id
        class_status = ClassStatus.objects.get(pk=data['class_status'])
        data['class_status'] = class_status.status_name
        location = Location.objects.get(pk=data['location']['id'])
        data['location'] = location.location
        data['location_id'] = location.id
        data['course_description'] = data['course_description'][0:25]
        data['default_course_rate'] = data['default_course_rate']
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        start = (start_date - timedelta(days=start_date.weekday()))
        end = (end_date - timedelta(days=end_date.weekday()))
        current = datetime.now().date()
        current_week = (current - timedelta(days=current.weekday()))
        if current_week >= end:
            completed = (end - start).days / 7
        else:
            completed = (current_week - start).days / 7

        data['no_of_weeks'] = (end - start).days / 7
      
        if completed < 0:
            completed = 0
        data['completed'] = completed
        data['id'] = data['id']
        return data


class CourseLocationSerializer(serializers.ModelSerializer):
    course_detail = CourseDetailSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = CourseLocation
        fields = (
            'course_detail',
            'location',
            'total_seats',
            'available_seats'
        )


# class CourseGroupDataSerializer(serializers.ModelSerializer):
#     course_detail = CourseDetailSerializer(read_only=True)
#     location = LocationSerializer(read_only=True)

#     class Meta:
#         model = CourseGroupData
#         fields = (
#             'course_detail',
#             'maximum_capacity'
#         )


class BookCourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCourseDetail
        fields = (
            'student',
            'course',
            'location',
            'start_date',
            'end_date',
            'notes',
            'id',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        student = Student.objects.get(pk=int(data['student']))
        data['student'] = student.first_name
        course = CourseDetail.objects.get(pk=int(data['course']))
        course_type = CourseType.objects.get(pk=course.course_type_id)
        data['course'] = course_type.course_name
        location = Location.objects.get(pk=int(data['location']))
        data['location'] = location.location
        data['start_date'] = data['start_date']
        data['end_date'] = data['end_date']
        data['id'] = data['id']
        return data


class BookCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCourseDetail
        fields = (
            'student',
            'course',
            'location',
            'start_date',
            'end_date',
            'notes',
            'id',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        student = StudentSerializer(
            Student.objects.get(pk=int(data['student'])))
        data['student'] = student.data
        course = CourseDetail.objects.get(pk=int(data['course']))
        course_type = CourseType.objects.get(pk=course.course_type_id)
        data['course'] = course_type.course_name
        location = Location.objects.get(pk=int(data['location']))
        data['location'] = location.location
        data['start_date'] = data['start_date']
        data['count'] = 0
        student_detail = Student.objects.get(
            first_name=student.data['first_name'])
        if Customer.objects.filter(pk=student_detail.customer_id).exists():
            count = BookCourseDetail.objects.filter(
                student__in=Student.objects.filter(
                    customer=Customer.objects.get(pk=student_detail.customer_id))).count()
            data['count'] = count
        data['end_date'] = data['end_date']
        data['id'] = data['id']
        return data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = (
            'id',
            'student',
            'course_detail',
            'start_date',
            'end_date',
            'title',
            'status',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print("data",data)
        student = Student.objects.get(pk=data['student'])
        # print(student)
       
        data['first_name'] = student.first_name
        data['last_name'] = student.last_name
        data['age'] = student.age
        if CourseDetail.objects.filter(pk=data['course_detail']).exists():
            course_age_group = CourseGroupData.objects.filter(
                course_detail=CourseDetail.objects.get(pk=data['course_detail'])).first()
            data['group'] = course_age_group.age.age
           
            data['start_time'] = course_age_group.start_time
       
            data['venue_name'] = course_age_group.course_detail.location.location
        else:
            data['group'] = None
            data['start_time'] = None
            data['venue_name'] = None
        data['date'] = data['start_date']
        return data


class EventDataSerializer(serializers.ModelSerializer):
    course_detail = CourseDetailSerializer(read_only=True)

    class Meta:
        model = Events
        fields = (
            'id',
            'student',
            'course_detail',
            'start_date',
            'end_date',
            'title',
            'status',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        dateandtime = parser.parse(data['start_date'])
        if data['start_date']:
            data['start_date'] = dateandtime.strftime("%d %b %Y")
        # data['start_date'] = datetime(data['start_date']).strftime('%A, %d %B')

        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'message',
            'to_role_id',
            'from_user_id',
            'created_date',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = User.objects.get(pk=data['from_user_id'])
        data['from_user_id'] = user.first_name
        dateandtime = parser.parse(data['created_date'])
        data['created_date'] = dateandtime.strftime("%d %b %Y At %H:%M %p")
        return data


class UserAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttendance
        fields = (
            'id',
            'student',
            'date',
            'title',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        student = Student.objects.get(pk=data['student'])
        data['student'] = student.first_name
        return data


class AccountRecordKeepingSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(read_only=True)

    class Meta:
        model = AccountRecordKeeping
        fields = (
            'id',
            'comment',
            'created_on',
            'active',
            'user',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        dateandtime = parser.parse(data['created_on'])
        data['created_on'] = dateandtime.strftime("%d %b %Y At %I:%M %p")
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'total',
        )


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    location = CourseLocationSerializer(read_only=True)
    course = CourseDetailSerializer(read_only=True)
    month = MonthSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'cart',
            'location',
            'course',
            'month',
        )


class RecentActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = (
            'verb',
            'actor_content_type',
            'timestamp',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserDataSerializer(
            User.objects.get(pk=data['actor_content_type'])).data
        dateandtime = parser.parse(data['timestamp'])
        data['timestamp'] = dateandtime.strftime("%d %b %Y At %H:%M %p")
        return data


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field='pk', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(
        many=False, slug_field='pk', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']


class MessageDataSerializer(serializers.ModelSerializer):
    sender = UserDataSerializer(read_only=True)
    receiver = UserDataSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        dateandtime = parser.parse(data['timestamp'])
        data['pk'] = data['id']
        data['timestamp'] = dateandtime.strftime("%d %b %Y At %I:%M %p")
        return data


class CourseDetailSerializerForBookingList(serializers.ModelSerializer):
    course_type = CourseTypeSerializer(read_only=True)
    # class_status = ClassStatusSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'course_type',
            'start_date',
            'end_date',
            'location',
            'default_course_rate',
            'id',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print("data",data)
        course_type = CourseType.objects.get(pk=data['course_type']['id'])
        data['course_type'] = course_type.course_name
        # class_status = ClassStatus.objects.get(pk=data['class_status'])
        # data['class_status'] = class_status.status_name
        location = Location.objects.get(pk=data['location']['id'])
        data['location'] = location.location
        data['default_course_rate'] = data['default_course_rate']
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        start = (start_date - timedelta(days=start_date.weekday()))
        end = (end_date - timedelta(days=end_date.weekday()))
        current = datetime.now().date()
        current_week = (current - timedelta(days=current.weekday()))
        if current_week >= end:
            completed = (end - start).days / 7
        else:
            completed = (current_week - start).days / 7
        data['no_of_weeks'] = (end - start).days / 7
        completed_for_status = completed
        data['completed'] = str(int(completed)) + \
            " of " + str(int(data['no_of_weeks']))
        if completed_for_status >= 8:
            class_status = "Closed"
        else:
            class_status = "Open"
        data['class_status'] = class_status
        data['id'] = data['id']
        return data

# class CourseGroupDataEditSerializer(serializers.ModelSerializer):
#     age = AgeSerializer(read_only=True)
#     class Meta:
#         model = CourseGroupData
#         fields = ("age", "start_time", "end_time", "from_drop_off_time", "from_pick_up_time", "to_drop_off_time", "to_pick_up_time", )

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         start_time = data['start_time']
#         d = datetime.strptime(start_time, "%H:%M:%S")
#         data['start_time'] = d.strftime("%I:%M %p")
#         end_time = data['end_time']
#         d = datetime.strptime(end_time, "%H:%M:%S")
#         data['end_time'] = d.strftime("%I:%M %p")
#         # from_drop_off_time = data['from_drop_off_time']
#         # d = datetime.strptime(from_drop_off_time, "%H:%M:%S")
#         # data['from_drop_off_time'] = d.strftime("%I:%M %p")
#         # from_pick_up_time = data['from_pick_up_time']
#         # d = datetime.strptime(from_pick_up_time, "%H:%M:%S")
#         # data['from_pick_up_time'] = d.strftime("%I:%M %p")
#         # to_drop_off_time = data['to_drop_off_time']
#         # d = datetime.strptime(to_drop_off_time, "%H:%M:%S")
#         # data['to_drop_off_time'] = d.strftime("%I:%M %p")
#         # to_drop_off_time = data['to_drop_off_time']
#         # d = datetime.strptime(to_drop_off_time, "%H:%M:%S")
#         # data['to_drop_off_time'] = d.strftime("%I:%M %p")
#         # to_pick_up_time = data['to_pick_up_time']
#         # d = datetime.strptime(to_pick_up_time, "%H:%M:%S")
#         # data['to_pick_up_time'] = d.strftime("%I:%M %p")

#         return data


class CourseGroupDataEditSerializer(serializers.ModelSerializer):
    age = AgeSerializer(read_only=True)

    class Meta:
        model = CourseGroupData
        fields = ("age", "start_time", "end_time", "from_drop_off_time",
                  "from_pick_up_time", "to_drop_off_time", "to_pick_up_time", )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if data['start_time']:
            start_time = data['start_time']
            d = datetime.strptime(start_time, "%H:%M:%S")
            data['start_time'] = d.strftime("%I:%M %p")
        if data['end_time']:
            end_time = data['end_time']
            d = datetime.strptime(end_time, "%H:%M:%S")
            data['end_time'] = d.strftime("%I:%M %p")
        # from_drop_off_time = data['from_drop_off_time']
        # d = datetime.strptime(from_drop_off_time, "%H:%M:%S")
        # data['from_drop_off_time'] = d.strftime("%I:%M %p")
        # from_pick_up_time = data['from_pick_up_time']
        # d = datetime.strptime(from_pick_up_time, "%H:%M:%S")
        # data['from_pick_up_time'] = d.strftime("%I:%M %p")
        # to_drop_off_time = data['to_drop_off_time']
        # d = datetime.strptime(to_drop_off_time, "%H:%M:%S")
        # data['to_drop_off_time'] = d.strftime("%I:%M %p")
        # to_drop_off_time = data['to_drop_off_time']
        # d = datetime.strptime(to_drop_off_time, "%H:%M:%S")
        # data['to_drop_off_time'] = d.strftime("%I:%M %p")
        # to_pick_up_time = data['to_pick_up_time']
        # d = datetime.strptime(to_pick_up_time, "%H:%M:%S")
        # data['to_pick_up_time'] = d.strftime("%I:%M %p")
        # print(data)
        return data


class CourseDetailEditSerializer(serializers.ModelSerializer):
    course_type = CourseTypeSerializer(read_only=True)
    # class_status = ClassStatusSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    # start_time = serializers.ReadOnlyField(source="course_group.start_time", read_only=True)
    course_coursegroupdata = CourseGroupDataEditSerializer(read_only=True)

    class Meta:
        model = CourseDetail
        fields = (
            'course_type',
            'start_date',
            'end_date',
            'location',
            'default_course_rate',
            'id',
            'logo',
            'course_coursegroupdata',


        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data["id"])
        course_type = CourseType.objects.get(pk=data['course_type']['id'])

        data['course_type'] = course_type.course_name
        # class_status = ClassStatus.objects.get(pk=data['class_status'])
        # data['class_status'] = class_status.status_name
        location = Location.objects.get(pk=data['location']['id'])
        data['location'] = location.location

        course_group = CourseGroupData.objects.filter(
            course_detail_id=data['id'])

        data['course_group'] = CourseGroupDataEditSerializer(
            course_group, many=True).data
        data['default_course_rate'] = data['default_course_rate']
        start_date = (datetime.strptime(data['start_date'], "%Y-%m-%d").date())
        start_date_with_day = start_date.strftime("%A %d %b %Y")
        day_filter = start_date.strftime("%A")
        data['day_filter'] = day_filter
        data['start_date_with_day'] = start_date_with_day

        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        start = (start_date - timedelta(days=start_date.weekday()))
        end = (end_date - timedelta(days=end_date.weekday()))
        current = datetime.now().date()
        current_week = (current - timedelta(days=current.weekday()))
        if current_week >= end:
            completed = (end - start).days / 7
        else:
            completed = (current_week - start).days / 7
        data['no_of_weeks'] = (end - start).days / 7
        completed_for_status = completed
        data['completed'] = str(int(completed)) + \
            " of " + str(int(data['no_of_weeks']))
        if completed_for_status >= 8:
            class_status = "Closed"
        else:
            class_status = "Open"
        data['class_status'] = class_status
        data['id'] = data['id']
        data['logo'] = data['logo']

        return data


class CourseDetailLocationAnalyticsSerializer(serializers.ModelSerializer):

    location = serializers.ReadOnlyField(source='location.location')

    class Meta:
        model = CourseDetail
        fields = (
            'id',
            'location',
        )


class GetCourseTypeWithCourseDetailSerializer(serializers.ModelSerializer):

    # course_details = CourseDetailDataSerializer(read_only=True, many=True)
    class Meta:
        model = CourseType
        fields = (
            'id',
            'course_name',
            'course_description',
            'course_title',
            "logo",
            # 'course_details',
        )


class GetCompanySerializer(serializers.ModelSerializer):
    # company = CompanySerializer(read_only=True)
    class Meta:

        model = Location
        fields = (
            "id",
            # "company"

        )


class CourseDetailsForBookingWithCourseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDetail
        fields = (
            "id",
            "logo",
            "start_date",
            "end_date",
            "street",
            "town",


        )


class AgeGroupsForBookingWithCourseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ages
        fields = (
            "id",
            "age_group_text",

        )


class AgesCourseGroupDataForBookingWithCourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ages
        fields = (
            "id",
            "age",
        )


class CourseGroupDataForBookingWithCourseTypeSerializer(serializers.ModelSerializer):
    age = AgesCourseGroupDataForBookingWithCourseTypeSerializer(read_only=True)

    class Meta:
        model = CourseGroupData
        fields = (
            "id",
            "start_time",
            "end_time",
            "from_drop_off_time",
            "from_pick_up_time",
            "to_drop_off_time",
            "to_pick_up_time",
            "maximum_capacity",
            "age",

        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if data['start_time']:
            start_time = data['start_time']
            d = datetime.strptime(start_time, "%H:%M:%S")
            data['start_time'] = d.strftime("%I:%M %p")
        if data['end_time']:
            end_time = data['end_time']
            d = datetime.strptime(end_time, "%H:%M:%S")
            data['end_time'] = d.strftime("%I:%M %p")
        if data['from_drop_off_time']:
            from_drop_off_time = data['from_drop_off_time']
            d = datetime.strptime(from_drop_off_time, "%H:%M:%S")
            data['from_drop_off_time'] = d.strftime("%I:%M %p")

        if data['from_pick_up_time']:
            from_pick_up_time = data['from_pick_up_time']
            d = datetime.strptime(from_pick_up_time, "%H:%M:%S")
            data['from_pick_up_time'] = d.strftime("%I:%M %p")

        if data['to_drop_off_time']:
            to_drop_off_time = data['to_drop_off_time']
            d = datetime.strptime(to_drop_off_time, "%H:%M:%S")
            data['to_drop_off_time'] = d.strftime("%I:%M %p")

        if data['to_pick_up_time']:
            to_pick_up_time = data['to_pick_up_time']
            d = datetime.strptime(to_pick_up_time, "%H:%M:%S")
            data['to_pick_up_time'] = d.strftime("%I:%M %p")

        return data


class CourseLocationForBookingWithCourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLocation
        fields = (
            "id",
            "available_seats",
        )


class BookingWithCourseTypeSerializer(serializers.ModelSerializer):

    course_name = serializers.ReadOnlyField(source='course_type.course_name')
    location = serializers.ReadOnlyField(source='location.location')
    surface = serializers.ReadOnlyField(source='playing_surface.surface')

    # age_group = AgeGroupsForBookingWithCourseTypeSerializer(read_only=True)

    course_details = CourseGroupDataForBookingWithCourseTypeSerializer(
        read_only=True, many=True)

    class Meta:
        model = CourseDetail
        fields = (
            "id",
            "logo",
            "course_name",
            "start_date",
            "end_date",
            "street",
            "town",
            "default_course_rate",
            "no_of_weeks",
            "location",
            "surface",
            "course_details",


        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data["id"])
        # course_type = CourseType.objects.get(pk=data['course_type']['id'])

        # data['course_type'] = course_type.course_name
        # class_status = ClassStatus.objects.get(pk=data['class_status'])
        # data['class_status'] = class_status.status_name
        # location = Location.objects.get(pk=data['location']['id'])
        # data['location'] = location.location

        course_group = CourseGroupData.objects.filter(
            course_detail_id=data['id'])

        data['course_group'] = CourseGroupDataEditSerializer(
            course_group, many=True).data
        data['default_course_rate'] = data['default_course_rate']
        start_date = (datetime.strptime(data['start_date'], "%Y-%m-%d").date())
        start_date_with_day = start_date.strftime("%A %d %b %Y")
        day_filter = start_date.strftime("%A")
        data['day_filter'] = day_filter
        data['start_date_with_day'] = start_date_with_day

        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        start = (start_date - timedelta(days=start_date.weekday()))
        end = (end_date - timedelta(days=end_date.weekday()))
        current = datetime.now().date()
        current_week = (current - timedelta(days=current.weekday()))
        if current_week >= end:
            completed = (end - start).days / 7
        else:
            completed = (current_week - start).days / 7
        data['no_of_weeks'] = (end - start).days / 7
        return data


class BookingWithCourseTypeExceptPreschoolSerializer(serializers.ModelSerializer):

    course_name = serializers.ReadOnlyField(source='course_type.course_name')
    location = serializers.ReadOnlyField(source='location.location')
    surface = serializers.ReadOnlyField(source='playing_surface.surface')

    course_details = CourseGroupDataForBookingWithCourseTypeSerializer(
        read_only=True, many=True)

    class Meta:
        model = CourseDetail
        fields = (
            "id",
            "logo",
            "course_name",
            "start_date",
            "end_date",
            "street",
            "event_type",
            "town",
            "default_course_rate",
            "no_of_weeks",
            "location",
            "surface",
            "course_details",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        course_group = CourseGroupData.objects.filter(
            course_detail_id=data['id'])

        data['course_group'] = CourseGroupDataEditSerializer(
            course_group, many=True).data
        data['default_course_rate'] = data['default_course_rate']
        start_date = (datetime.strptime(data['start_date'], "%Y-%m-%d").date())
        end_date_for_booking = (datetime.strptime(
            data['end_date'], "%Y-%m-%d").date())
        start_date_with_day = start_date.strftime("%d %b %Y")
        end_date_with_day = end_date_for_booking.strftime("%d %b %Y")
        day_filter = start_date.strftime("%A")
        data['day_filter'] = day_filter
        data['start_date_with_day'] = start_date_with_day
        data['end_date_for_booking'] = end_date_with_day

        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        start = (start_date - timedelta(days=start_date.weekday()))

        end_date_for_week_count = end_date + timedelta(days=1)

        end = (end_date - timedelta(days=end_date.weekday()))
        number_of_days = (end_date_for_week_count-start_date).days
        # print(number_of_days)
        days_calculated = number_of_days/7
        # print(days_calculated)

        if (number_of_days % 7) > 0:

            calculated_date = int(math.ceil(days_calculated))
            data['weekCountForRendering'] = calculated_date

        else:
            calculated_date = int(math.ceil(days_calculated))

        data['weekCountForRendering'] = calculated_date

        # week_calculated = int(math.ceil(days_calculated+1))

        current = datetime.now().date()

        current_week = (current - timedelta(days=current.weekday()))

        if current_week >= end:

            completed = int(math.ceil((end-start).days/7))

        else:
            completed = (current_week - start).days / 7

        data['no_of_weeks'] = (end - start).days / 7
        return data


class BookingCustomerStudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingCustomerStudentDetails
        fields = (
            "student",
            "customer",
            "location",
            "course",
            "start_date",
            "end_date",

        )


class RecentlyRegisterStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "ages",
            "customer",


        )


class CourseLocationForAvailableSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLocation
        fields = ("total_seats", "available_seats",)


class CourseDetaiForAvailableSeatsSerializer(serializers.ModelSerializer):

    course_location = CourseLocationForAvailableSeatsSerializer(
        read_only=True, many=True)

    class Meta:

        model = CourseDetail
        fields = ("id",
                  "course_location",
                  )


class EventWeekSerializer(serializers.ModelSerializer):
    """event week """
    class Meta:
        model = EventWeek
        fields = "__all__"

    def create(self, validated_data):
        event_week = EventWeek.objects.create(**validated_data)
        event_week.save()
        return event_week


class DayWiseWeekDetailsSerializer(serializers.ModelSerializer):
    """Day wise Week Detail"""
    class Meta:
        model = DayWiseWeekDetails
        fields = "__all__"

    def create(self, validated_data):
        day_wise_week_details = DayWiseWeekDetails.objects.create(
            **validated_data)
        day_wise_week_details.save()
        return day_wise_week_details


class OrderSerializer(serializers.ModelSerializer):
    """Order"""
    class Meta:
        model = Order
        fields = "__all__"

    # def create(self, validated_data):
    #     order = Order.objects.create(**validated_data)
    #     order.save()
    #     return order


class NurseryAndWeeklyStudentOrderDetailsSerializer(serializers.ModelSerializer):
    """Nursery and weekly student order details"""
    class Meta:
        model = NurseryAndWeeklyStudentOrderDetails
        fields = "__all__"

    def create(self, validated_data):
        nursery_and_weekly_student_order_details = NurseryAndWeeklyStudentOrderDetails.objects.create(
            **validated_data)
        nursery_and_weekly_student_order_details.save()
        return nursery_and_weekly_student_order_details


class OrderSummarySerializer(serializers.ModelSerializer):
    """Order Summary"""
    class Meta:
        model = OrderSummary
        fields = ('id', 'order',
                  'nursery_and_weekly_student_order_details', 'payment')

    def create(self, validated_data):
        order_summary = OrderSummary.objects.create(**validated_data)
        order_summary.save()
        return order_summary


class PriceMatrixSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceMatrix
        fields = "__all__"


class PreschoolBookingPriceFormSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        models = Order
        fields = (
            "customer",
            "total_cost",

        )


class OrderSummaryForPreschoolSerializer(serializers.ModelSerializer):

    class Meta:
        models = OrderSummary
        fields = ("id", "order", "day_wise_week_details", "payment")


class NestedOrderOrderSummarySerializer(serializers.ModelSerializer):
    order_summary = OrderSummarySerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id", "event_week", "customer", "total_cost", "price_matrix", "discounted_amount", "order_summary",
        )

    def create(self, validated_data):
        order_summary = validated_data.pop('order_summary')
        order = Order.objects.create(**validated_data)
        for order_summary_data in order_summary:
            OrderSummary.objects.create(
                order=order, **order_summary_data)
        return order


# class NestedOrderOrderSummarySerializer(serializers.ModelSerializer):
#     order = OrderSummaryForPreschoolSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = (
#             "id", "event_week", "customer", "total_cost", "price_matrix", "discounted_amount" , "order",
#         )

#     def create(self, validated_data):
#         order_summary = validated_data.pop('order')
#         order = Order.objects.create(**validated_data)
#         for order_summary_data in order_summary:
#             OrderSummary.objects.create(
#                 order=order, **order_summary_data)
#         return order


class NurseryAndWeeklyStudentOrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NurseryAndWeeklyStudentOrderDetails
        fields = ("student", "customer",)


class OrderSummaryForStudentPaymentPaid(serializers.ModelSerializer):

    nursery_and_weekly_student_order_details = NurseryAndWeeklyStudentOrderDetailsSerializer(
        read_only=True)

    class Meta:
        model = OrderSummary
        fields = ("id", "order",
                  "nursery_and_weekly_student_order_details", "payment",)

class GetAllCompaniesDataSerializer(serializers.ModelSerializer):
    """Get all companies data"""
    class Meta:
        model = Company
        fields = "__all__"

class GetLocationBYCompany(serializers.ModelSerializer):
    """Get location by company"""
    class Meta:
        model = Location
        fields = "__all__"

class CourseEditSerializer(serializers.ModelSerializer):
    """Course Edit Functionality serializer"""
    class Meta:
        model = CourseDetail
        fields = ("course_type_id", "logo", "start_date", "end_date", "default_course_rate", "course_description", "event_type_id", "class_status_id",)
        # fields = ("course_type","logo", "default_course_rate", "start_date",)


class PriceMatricForDynamicDataSerializer(serializers.ModelSerializer): 
    """serialzier to Save course prices in price matrix"""

    class Meta:
        model = PriceMatrix
        fields = ("version", "course_detail", "single_day",)

class PriceMatricForDynamicDataForHolidaySerializer(serializers.ModelSerializer): 
    """serialzier to Save course prices in price matrix"""

    class Meta:
        model = PriceMatrix
        fields = ("version", "course_detail", "single_day", "two_days", "three_days", "four_days", "five_days",)

class CourseDetailByLocationSerializer(serializers.ModelSerializer):
    """Serializer to get course detail by id"""

    class Meta:
        model = CourseDetail
        fields = ("id","start_date", "end_date",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(data)
 
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        start = (start_date - timedelta(days=start_date.weekday()))
        end = (end_date - timedelta(days=end_date.weekday()))
        current = datetime.now().date()
        current_week = (current - timedelta(days=current.weekday()))
        if current_week >= end:
            completed = (end - start).days / 7
        else:
            completed = (current_week - start).days / 7

        data['no_of_weeks'] = (end - start).days / 7
      
        if completed < 0:
            completed = 0
        data['completed'] = completed
    
        return data