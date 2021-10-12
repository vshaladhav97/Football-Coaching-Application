from rest_framework import serializers
from .models import Coach, CoachDocuments
from customer.models import User
from customer.serializer import UserSerializer
from course.serializer import CourseDetailSerializer


class CoachSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coach
        fields = (
            'first_name',
            'last_name',
            'email',
            'mobile',
            'landline',
            'address',
            'postal_code',
            'id',
            'town',
            'profile_image',
            # 'profile_image',
        )




class CoachUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Coach
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

class CoachAnalyticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = (
            'user',
            'first_name',
            'last_name'
        )

class CoachListAnalyticsSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = (
            'id',
            'first_name',
     
        )


class CoachDataTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = (
            'user',
            'profile_image',
            'first_name',
            'last_name',
            'town',
            'postal_code',
            'address',
            'id',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = User.objects.get(pk=data['user'])
        data['job_type'] = user.role.name
        return data


class CoachDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachDocuments
        fields = (
            'file_path',
        )


# class EventDataSerializer(serializers.ModelSerializer):
#     course_detail = CourseDetailSerializer(read_only=True)

#     class Meta:
#         model = Events
#         fields = (
#             'id',
#             'student',
#             'course_detail',
#             'start_date',
#             'end_date',
#             'title',
#             'status',
#         )

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         dateandtime = parser.parse(data['start_date'])
#         data['start_date'] = dateandtime.strftime("%d %b %Y")
#         # data['start_date'] = datetime(data['start_date']).strftime('%A, %d %B')
#         return data