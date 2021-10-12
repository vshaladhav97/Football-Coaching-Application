from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from ..models import Customer, User, Student, Role, query_users_by_args, query_students_by_args, CustomerDocuments
from course.models import BookCourseDetail, UserAttendance, Events, Notification, Cart, CartItem, CourseDetail
from customer.decorator import check_role_permission
from master.models import CourseType, CourseWiseSuitableLocation
from django.db.models import Count
from first_kick_management.settings import logger
import json
import datetime


class DashboardView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Get dashboard page
        """
        try:
            login = True if "login" in request.session else False
            if "email" in request.session:
                user = User.objects.get(email__iexact=request.session['email'])
                role = str(user.role)
                if role == "Customer" or role == "Coach Manager" or role == "Head Coach":
                    return render(request, 'dashboard.html', {"login": login})
            return render(request, 'management_dashboard.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class DashboardPageView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Get dashboard data
        """
        try:
            if request.user.role is None:
                return JsonResponse({"message": "identify role", 'data': str(request.user.role)}, status=204)
            return JsonResponse({"message": "dashboard data", 'data': str(request.user.role)})
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class DashboardCountsView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get dashboard data
        """
        try:
            student = classes = absent = rebook = 0
            all_courses = CourseDetail.objects.all().count()
            total_student_booked = BookCourseDetail.objects.all().count()
            if Customer.objects.filter(email=request.user).exists():
                customer = Customer.objects.get(email=request.user)
                student = Student.objects.filter(customer=customer).count()

                # cancellation_count =
                classes = BookCourseDetail.objects.filter(student__in=Student.objects.filter(customer=customer).values('id')).count()
                absent = UserAttendance.objects.filter(
                    student__in=Student.objects.filter(customer=customer).values('id')).count()
                rebook = Events.objects.filter(student__in=Student.objects.filter(customer=customer).values('id')).count()
            today = datetime.datetime.now().date()
            notifications = Notification.objects.filter(created_date=today, viewed=False).count()
            if Cart.objects.filter(created_by=request.user).exists():
                cart = Cart.objects.get(created_by=request.user)
                cart_count = CartItem.objects.filter(cart=cart, purchased=False).count()
            else:
                cart_count = 0

            weekly_football = CourseDetail.objects.filter(course_type=CourseType.objects.get(course_name="Evening Development")).count()
            nursery = CourseDetail.objects.filter(course_type=CourseType.objects.get(course_name="Nursery")).count()
            holiday = CourseDetail.objects.filter(course_type=CourseType.objects.get(course_name="Holiday Camp")).count()
            evening_development_locations = CourseWiseSuitableLocation.objects.filter(course_type=CourseType.objects.get(course_name="Evening Development")).count()
            nursery_locations = CourseWiseSuitableLocation.objects.filter(course_type=CourseType.objects.get(course_name="Nursery")).count()
            holiday_locations = CourseWiseSuitableLocation.objects.filter(course_type=CourseType.objects.get(course_name="Holiday Camp")).count()

            data = {
                    'student': student,
                    'classes': classes,
                    'absents': absent,
                    'rebooked': rebook,
                    'notification': notifications,
                    'cart_count': cart_count,
                    'all_courses': all_courses,
                    'total_students_booked': total_student_booked,
                    'weekly_football_count': weekly_football,
                    'nursery': nursery,
                    'holiday': holiday,
                    'evening_development_locations': evening_development_locations,
                    'nursery_locations': nursery_locations,
                    'holiday_locations': holiday_locations
            }
            return JsonResponse({"message": "dashboard data", 'data': json.dumps(data)})
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)