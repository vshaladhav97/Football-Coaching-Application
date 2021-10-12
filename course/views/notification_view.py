from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from ..serializer import (CourseDetailSerializer, CourseLocationSerializer,
                         BookCourseDetailSerializer, EventSerializer,
                         NotificationSerializer, UserAttendanceSerializer,
                         CourseDataTableSerializer, BookCourseSerializer,
                         CourseListingDataSerializer, AccountRecordKeepingSerializer)
from ..models import (CourseDetail, CourseLocation, CourseMonths, Events,
                     Notification, BookCourseDetail, UserAttendance, AccountRecordKeeping,
                     query_course_by_args, query_courses_booked_by_args)
from customer.models import Student, User, Role, Customer
from customer.decorator import check_role_permission
from django.db.models import Q
import csv
import datetime
from first_kick_management.settings import logger


class NotificationPageView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Get page
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'notification.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class NotificationView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get notification
        """
        try:
            today = datetime.datetime.now().date()
            serializer = NotificationSerializer(
                Notification.objects.filter(
                    Q(created_date=today)), many=True)
            return JsonResponse({"message": "list of notification", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        try:
            request.data._mutable = True
            request.data['from_user_id'] = request.user.id
            request.data._mutable = False
            notification_serializer = NotificationSerializer(data=request.data)
            if notification_serializer.is_valid(
                    raise_exception=True):
                notification_serializer.validated_data['message'] = request.data['message']
                notification_serializer.validated_data['from_user_id'] = request.user
                if request.data['user_id'] is not None and request.data['user_id'] != "0":
                    notification_serializer.validated_data['to_user_id'] = User.objects.get(pk=request.data['user_id'])
                notification_serializer.validated_data['to_role_id'] = Role.objects.get(pk=Role.objects.get(name="Management").id)
                notification_serializer.save()
            return JsonResponse({"message": "course booked"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ExportBookedCourses(generics.GenericAPIView):
    def get(self,request):
        try:
            response = HttpResponse(content_type='text/csv')
            booked_courses = BookCourseDetail.objects.all()
            response['Content-Disposition'] = 'attachment; filename="export.csv"'
            writer = csv.writer(response)
            writer.writerow(['STUDENT_FIRST_NAME', 'COURSE_DESCRIPTION', 'START_DATE', 'END_DATE'])
            for member in BookCourseDetail.objects.all().values_list(
                    'student__first_name', 'course__course_description', 'start_date', 'end_date',
                    'notes'):
                writer.writerow(member)
            return response
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class GetTokenView(generics.GenericAPIView):
    def get(self, request):
        try:
            booked_courses = BookCourseDetail.objects.get(student=request.GET.get('student'))
            return JsonResponse({"message": "tokens available", "tokens": booked_courses.tokens}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class NotificationViewedView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Notification viewed
        """
        try:
            today = datetime.datetime.now().date()
            Notification.objects.filter(to_user_id=request.user.id, created_date=today).update(viewed=True)
            return JsonResponse({"message": "Notification viewed"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
