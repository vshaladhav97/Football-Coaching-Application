from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from ..serializer import (CourseDetailSerializer, CourseLocationSerializer,
                         BookCourseDetailSerializer, EventSerializer,
                         NotificationSerializer, UserAttendanceSerializer,
                         CourseDataTableSerializer, BookCourseSerializer,
                         CourseListingDataSerializer, AccountRecordKeepingSerializer)
from ..models import (CourseDetail, CourseLocation, CourseMonths, Events,
                     Notification, BookCourseDetail, UserAttendance, AccountRecordKeeping,
                     query_course_by_args, query_courses_booked_by_args)
from customer.decorator import check_role_permission
from first_kick_management.settings import logger


class AccountRecordView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt Booked course add view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'account_record/record_keep.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class AccountRecordDataView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get all comments
        """
        try:
            serializer = AccountRecordKeepingSerializer(AccountRecordKeeping.objects.all(), many=True)
            return JsonResponse({"message": "list of comments", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Add comment
        """
        try:
            AccountRecordKeeping.objects.create(
                user=request.user,
                comment=request.data['comment']
            )
            return JsonResponse({"message": "comment added successfully"}, status=201)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ShopView(generics.GenericAPIView):
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'shop-elements.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')
