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
from master.models import (AgeGroup, AddressDetail, CourseType, EventType,
                           ClassStatus, Months, Location)
from master.serializer import LocationSerializer
from customer.models import Student, User, Role, Customer
from coach.models import Coach
from customer.decorator import check_role_permission
from django.db.models import Q
from first_kick_management.settings import logger


class GetClassOnMonth(generics.GenericAPIView):
    def post(self, request):
        """
        Get courses through location
        """
        try:
            location = LocationSerializer(Location.objects.get(pk=request.data['location_id']))

            serializer = CourseDetailSerializer(
                CourseDetail.objects.filter(Q(
                    pk__in=CourseLocation.objects.filter(
                        location=location.data['id']).values('course_detail')) & Q(
                    pk__in=CourseMonths.objects.filter(
                        month__id=request.data['month']).values('course_detail')
                ) & Q(
                    pk=request.data['course_id']
                )), many=True)
            return JsonResponse({"message": "list of courses", "data": serializer.data, "location": location.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class AddStudentToCourseView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Get page
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/add_student_to_course.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class EventsForCoachView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get all events
        """
        try:
            coach = Coach.objects.get(user=request.user)
            courses = CourseLocation.objects.filter(coach=coach).values('course_detail')
            serializer = EventSerializer(Events.objects.filter(
                course_detail__in=courses
            ), many=True)
            return JsonResponse({"message": "list of events", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        try:
            booked_course = BookCourseDetail.objects.get(student=Student.objects.get(pk=request.data['student']))
            booked_course.tokens -= 1
            booked_course.save()
            course = CourseDetail.objects.get(pk=booked_course.course_id)
            # request.data['course_detail'] = course
            Events.objects.create(
                student=Student.objects.get(pk=request.data['student']),
                course_detail=course,
                title=request.data['title'],
                date=request.data['date']
            )

            return JsonResponse({"message": "event added"}, status=201)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class EventsForCustomerView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get all events
        """
        try:
            user_attendance = UserAttendance.objects.filter(user=request.user)
            serializer = UserAttendanceSerializer(user_attendance, many=True)
            return JsonResponse({"message": "list of all events", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        try:
            attendance_serializer = UserAttendanceSerializer(data=request.data)

            if attendance_serializer.is_valid(
                    raise_exception=True):
                attendance_serializer.validated_data['user'] = request.user
                attendance_serializer.validated_data['student'] = Student.objects.get(pk=request.data['student'])
                attendance_serializer.validated_data['date'] = request.data['date']
                attendance_serializer.save()
                booked_courses = BookCourseDetail.objects.get(student=request.data['student'])
                booked_courses.tokens += 1
                booked_courses.save()
                student = Student.objects.get(pk=request.data['student'])

                # send_mail(
                #     'Notification',
                #     student.first_name + "is going to be absent on" + str(request.data['date']),
                #     'umeshdevadiga555@gmail.com',
                #     ['umesh1996d@gmail.com'],
                #     fail_silently=False,
                # )
            return JsonResponse({"message": "Attendance added"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookedEventsForCustomerView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get all events
        """
        try:
            student = Student.objects.filter(customer=Customer.objects.get(email=request.user)).values('id')
            serializer = BookCourseSerializer(BookCourseDetail.objects.filter(student_id__in=student), many=True)
            return JsonResponse({"message": "list of events", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class StudentBookedView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BookCourseDetailSerializer

    def get(self, request):
        try:
            # customer = Customer.objects.get(email=request.user)
            # student = Student.objects.filter(customer=Customer.objects.get(email=request.user)).values('id')
            # booked_course = BookCourseDetail.objects.filter(student__in=Student.objects.filter(pk__in=student))
            if Customer.objects.filter(email=request.user).exists():
                serializer = BookCourseSerializer(BookCourseDetail.objects.filter(
                    student__in=Student.objects.filter(
                        customer=Customer.objects.get(email=request.user))), many=True)
                return JsonResponse({"message": "list of students", "data": serializer.data}, status=200)
            return JsonResponse({"message": "get student", "data": ""}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
