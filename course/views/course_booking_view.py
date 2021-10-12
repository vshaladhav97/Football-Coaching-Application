import json
import re
from django.core.serializers import serialize
from django.db.utils import Error
from django.http import request
from django.shortcuts import render
from rest_framework import generics, serializers
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..serializer import (CourseDetailSerializer,
                          BookCourseDetailSerializer, EventSerializer,
                           BookCourseSerializer,
                          CourseDetailSerializerForBookingList, CourseDetailEditSerializer, BookingWithCourseTypeSerializer,
                          BookingWithCourseTypeExceptPreschoolSerializer, RecentlyRegisterStudentSerializer,
                          CourseDetaiForAvailableSeatsSerializer, EventWeekSerializer, DayWiseWeekDetailsSerializer, OrderSerializer,
                          OrderSummarySerializer, PriceMatrixSerializer, PreschoolBookingPriceFormSubmissionSerializer, 
                          NurseryAndWeeklyStudentOrderDetailsSerializer, OrderSummaryForStudentPaymentPaid, GetLocationBYCompany, PriceMatricForDynamicDataSerializer,
                          PriceMatricForDynamicDataForHolidaySerializer)
from ..models import (CourseDetail, CourseLocation, Events, EventWeek, DayWiseWeekDetails, Order, OrderSummary, BookCourseDetail, UserAttendance, PriceMatrix, 
                        query_courses_booked_by_args, query_events_by_args, query_course_by_args_for_booking_list, NurseryAndWeeklyStudentOrderDetails)
from master.models import (Location)
from customer.models import Student, Customer
from customer.decorator import check_role_permission
import datetime
from first_kick_management.settings import logger
from rest_framework.views import APIView
from django.db import transaction
from customer.views import save_payment_data
from customer.models import Payment
import pprint


class BookedCoursePageView(generics.GenericAPIView):

    def get(self, request):
        """
        Get page
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'bookedcourses/booked_courses_listing.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class BookedCoursesList(generics.GenericAPIView):
    serializer_class = BookCourseDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get all courses
        """
        try:
            datatable_server_processing = query_courses_booked_by_args(
                request, **request.query_params)
            serializer = BookCourseDetailSerializer(
                datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookedCoursesAddPage(generics.GenericAPIView):
    def get(self, request):
        """
        Gwt Booked course add view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'bookedcourses/booked_course_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class BookedCourseAddView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Book course
        """
        try:
            end_date = datetime.datetime.strptime(
                request.data['end_date'], '%Y-%m-%d')
            start_date = datetime.datetime.strptime(
                request.data['start_date'], '%Y-%m-%d')
            request.data._mutable = True
            request.data['end_date'] = end_date.strftime("%Y-%m-%d")
            request.data['start_date'] = start_date.strftime("%Y-%m-%d")
            book_course_seriliazer = BookCourseDetailSerializer(
                data=request.data)
            if book_course_seriliazer.is_valid(
                    raise_exception=True):
                book_course_seriliazer.validated_data['student'] = Student.objects.get(
                    pk=request.data['student'])
                book_course_seriliazer.validated_data['course'] = CourseDetail.objects.get(
                    pk=request.data['course'])
                book_course_seriliazer.validated_data['location'] = Location.objects.get(
                    pk=request.data['location'])
                book_course_seriliazer.validated_data['start_date'] = request.data['start_date']
                book_course_seriliazer.validated_data['end_date'] = request.data['end_date']
                book_course_seriliazer.save()
            return JsonResponse({"message": "course booked"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookedCourseEditView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt Booked course edit view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'bookedcourses/booked_course_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class BookedCourseDetailView(generics.GenericAPIView):
    serializer_class = BookCourseDetailSerializer

    def get_object(self, pk):
        try:
            return BookCourseDetail.objects.get(pk=pk)
        except BookCourseDetail.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Get all courses
        """
        try:
            serializer = BookCourseDetailSerializer(
                BookCourseDetail.objects.get(pk=pk))
            return JsonResponse({"message": "booked course data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update course
        """
        try:
            booked_course = self.get_object(pk)
            end_date = datetime.datetime.strptime(
                request.data['end_date'], '%Y-%m-%d')
            start_date = datetime.datetime.strptime(
                request.data['start_date'], '%Y-%m-%d')
            request.data._mutable = True
            request.data['end_date'] = end_date.strftime("%Y-%m-%d")
            request.data['start_date'] = start_date.strftime("%Y-%m-%d")
            serializer = BookCourseDetailSerializer(
                booked_course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete course
        """
        try:
            booked_course = self.get_object(pk)
            if booked_course:
                booked_course.delete()
                message = "Course deleted successfully"
                return JsonResponse({'message': message}, status=200)
            return JsonResponse({'message': "Course not found"}, status=401)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class GetBookedCoursesForCustomer(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BookCourseDetailSerializer

    def get(self, request):
        try:
            # customer = Customer.objects.get(email=request.user)
            # student = Student.objects.filter(customer=Customer.objects.get(email=request.user)).values('id')
            # booked_course = BookCourseDetail.objects.filter(student__in=Student.objects.filter(pk__in=student))
            if Customer.objects.filter(email=request.user).exists():

                booked_courses = BookCourseDetail.objects.filter(student__in=Student.objects.filter(
                    customer=Customer.objects.get(email=request.user))).values('course').distinct()

                data = []
                for course in booked_courses:

                    booked_course = BookCourseDetail.objects.filter(student__in=Student.objects.filter(
                        customer=Customer.objects.get(email=request.user)), course_id=course['course']).first()
                    course_name = booked_course.course.course_type.course_name
                    no_of_students = BookCourseDetail.objects.filter(student__in=Student.objects.filter(
                        customer=Customer.objects.get(email=request.user)), course_id=course['course']).count()
                    start_date = booked_course.start_date
                    end_date = booked_course.end_date

                    dict_data = {
                        'course_name': course_name,
                        'no_of_students': no_of_students,
                        'start_date': start_date,
                        'end_date': end_date
                    }

                    data.append(dict_data)

                serializer = BookCourseSerializer(BookCourseDetail.objects.filter(
                    student__in=Student.objects.filter(
                        customer=Customer.objects.get(email=request.user))), many=True)
                return JsonResponse({"message": "get student", "data": data}, safe=False, status=200)
            return JsonResponse({"message": "get student", "data": ""}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class UpcomingCoursesView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BookCourseDetailSerializer

    def get(self, request):
        try:
            if Customer.objects.filter(email=request.user).exists():

                booked_courses = BookCourseDetail.objects.filter(student__in=Student.objects.filter(
                    customer=Customer.objects.get(email=request.user))).values('course').distinct()

                cour_ids = []
                for course in booked_courses:
                    cour_ids.append(course['course'])

                upcoming_courses = CourseDetail.objects.exclude(
                    pk__in=cour_ids).filter(class_status__status_name="Active")

                data = []
                for upcoming in upcoming_courses:
                    dict_data = {
                        'course_name': upcoming.course_type.course_name,
                        'no_of_students': 0,
                        'start_date': upcoming.start_date,
                        'end_date': upcoming.end_date
                    }

                    data.append(dict_data)
                return JsonResponse({"message": "get upcoming courses", "data": data}, safe=False, status=200)
            return JsonResponse({"message": "get student", "data": ""}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookCourseView(generics.GenericAPIView):

    def post(self, request):
        """
        Book course for students
        """
        try:
            book_course_detail_serializer = BookCourseDetailSerializer(
                data=request.data)
            if book_course_detail_serializer.is_valid(
                    raise_exception=True):

                book_course_detail_serializer.validated_data['student'] = Student.objects.get(
                    pk=request.data['student'])
                book_course_detail_serializer.validated_data['course'] = CourseDetail.objects.get(
                    pk=request.data['course'])
                book_course_detail_serializer.validated_data['location'] = Location.objects.get(
                    pk=request.data['location'])
                book_course_detail_serializer.save()
                courseLocation = CourseLocation.objects.get(
                    location=request.data['location'], course_detail=request.data['course'])
                courseLocation.available_seats -= 1
                courseLocation.save()
            return JsonResponse({"message": "course booked"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ClassRegisterView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Class registered students
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/class_register.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ClassRegisterDataView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get attendance list
        """
        try:
            print("in try")
            print(request)
            datatable_server_processing = query_events_by_args(
                request, **request.query_params)
            print("datatable",datatable_server_processing)
            serializer = EventSerializer(
                datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            print(result)
            return Response(result)
        # try:
        #     date = datetime.datetime.date()
        #     serializer = EventSerializer(Events.objects.filter(start_date=date), many=True)
        #     return JsonResponse({'message': 'students list', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Save presenties
        """
        try:
            event = Events.objects.get(pk=request.data['id'])
            event.status = request.data['status']
            event.save()

            if request.data['status'] == "absent":
                UserAttendance.objects.create(
                    user=request.user,
                    student=Student.objects.get(pk=event.student.id),
                    date=event.start_date
                )

            return JsonResponse({"message": "status updated"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

# @check_role_permission()


def course_booking(request):
    login = True if "login" in request.session else False
    return render(request, 'course/booking_list.html', {"login": login})


def course_booking1(request):
    login = True if "login" in request.session else False
    return render(request, 'course/booking_edit.html', {"login": login})


def registration1(request):
    login = True if "login" in request.session else False
    return render(request, 'course/customer_registration_part_1.html', {"login": login})


class CourseBookingList(generics.GenericAPIView):

    # def get(self, request):
    #     course_detail = CourseDetail.objects.all()
    #     serializer = CourseDetailSerializerForBookingList(course_detail, many=True)
    #     return Response(serializer.data)
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get attendance list
        """
        try:
            datatable_server_processing = query_course_by_args_for_booking_list(
                request, **request.query_params)
            serializer = CourseDetailSerializerForBookingList(
                datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
        # try:
        #     date = datetime.datetime.date()
        #     serializer = EventSerializer(Events.objects.filter(start_date=date), many=True)
        #     return JsonResponse({'message': 'students list', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)



# class BookingEditData(generics.GenericAPIView):
#     serializer_class = CourseDetailEditSerializer

#     def get_object(self, pk):
#         try:
#             return CourseDetail.objects.get(pk=pk)
#         except CourseDetail.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         """
#         Get all courses
#         """
#         try:
#             serializer = CourseDetailEditSerializer(CourseDetail.objects.get(pk=pk))
#             return JsonResponse({"message": "course data", "data": serializer.data}, status=200)
#         except Exception as e:
#             logger.error(e, exc_info=True)
#             return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

#     def put(self, request, pk):
#         """
#         Update course
#         """
#         try:
#             course = self.get_object(pk)
#             serializer = CourseDetailSerializer(course, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse({"message": "course updated", 'data': serializer.data}, status=200)
#         except Exception as e:
#             logger.error(e, exc_info=True)
#             return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

#     def delete(self, request, pk):
#         """
#         Delete course
#         """
#         try:
#             course = self.get_object(pk)
#             if course:
#                 course.delete()
#                 message = "Course deleted successfully"
#                 return JsonResponse({'message': message}, status=200)
#             return JsonResponse({'message': "Course not found"}, status=401)
#         except Exception as e:
#             logger.error(e, exc_info=True)
#             return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookingEditData(generics.GenericAPIView):
    serializer_class = CourseDetailEditSerializer

    def get_object(self, pk):
        try:
            return CourseDetail.objects.get(pk=pk)
        except CourseDetail.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Get all courses
        """
        try:
            serializer = CourseDetailEditSerializer(
                CourseDetail.objects.get(pk=pk))

            return JsonResponse({"message": "course data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)

            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update course
        """
        try:
            course = self.get_object(pk)
            serializer = CourseDetailSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "course updated", 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete course
        """
        try:
            course = self.get_object(pk)
            if course:
                course.delete()
                message = "Course deleted successfully"
                return JsonResponse({'message': message}, status=200)
            return JsonResponse({'message': "Course not found"}, status=401)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookingByCourseType(generics.GenericAPIView):

    def get(self, request, pk, dk):
        try:
            # print(request.data)
            course_type = CourseDetail.objects.filter(
                location_id=pk, id=dk)
            serializer = BookingWithCourseTypeSerializer(
                course_type, many=True)
            return JsonResponse({"data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookingByCourseTypeExceptPreschool(generics.GenericAPIView):

    def get(self, request, pk, dk):
        try:
            # print(request.data)
            course_type = CourseDetail.objects.filter(
                location_id=pk, id=dk)
            serializer = BookingWithCourseTypeExceptPreschoolSerializer(
                course_type, many=True)
            return JsonResponse({"data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    # def get(self, request, pk):
    #     """
    #     Get all weekdays
    #     """
    #     try:

    #         # serializer = MonthSerializer(Months.objects.all(), many=True)
    #         data = list(CourseDetail.objects.filter(course_type__id=pk).values("location", "location__location", "location__address_line_1", "location__town", "location__postal_code", "location__playing_surface__surface", "location__logo", "start_date",
    #                                                                             "end_date", "default_course_rate", "no_of_weeks", "age_group_id").distinct())
    #         # print(data)

    #         # return JsonResponse(serialize("json", data), status=200, safe=False)
    #         return JsonResponse({"company_name": data}, status=200)
    #     except Exception as e:
    #         logger.error(e, exc_info=True)
    #         print(e)
    #         return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class BookingCustomerStudentDetails(generics.GenericAPIView):
    def post(self, request):
        try:
            json_data = request.data

            customer_data = {"student": json_data["user_id"], "customer": json_data["first_name"], "location": json_data["last_name"], "course": json_data["email"],
                             "start_date": json_data["mobile"], "landline": json_data["landline"]}
            # print(request.data)
            customer = BookingCustomerStudentDetails(data=customer_data)
            # print(customer.is_valid())
            if customer.is_valid():
                customer.save()
                # print(customer)
                customer["id"].value
                return JsonResponse(customer["id"].value, status=200, safe=False)
            else:
                # print(customer.errors)
                return JsonResponse(customer.data, status=400)
        except Exception as e:
            # print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class RecentlyBookedStudents(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            student = Student.objects.order_by('-id')[0:pk]
            serializer = RecentlyRegisterStudentSerializer(student, many=True)
            return JsonResponse({"data": serializer.data}, status=200)
        except Exception as e:
            # print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CourseDetaiForAvailableSeatsView(generics.GenericAPIView):

    def get(self, request):
        try:
            seats = CourseDetail.objects.all()
            serializer = CourseDetaiForAvailableSeatsSerializer(
                seats, many=True)
            return JsonResponse({"data": serializer.data}, status=200)
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class AvailableSeatCalculater(generics.GenericAPIView):

    def post(self, request):
        json_data = request.data

        customer_data = {
            "total_seats": json_data["total_seats"], "available_seats": json_data["available_seats"]}
        seats = CourseLocation.objects.get(course_detail_id=1)
        seats.total_seats = json_data["total_seats"]
        seats.save()
        serializer = CourseDetaiForAvailableSeatsSerializer(
            customer_data, many=True)
        return JsonResponse({"data": seats.data}, status=200)


class PriceMatrixDetails(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            price_matrix = PriceMatrix.objects.filter(course_detail_id=pk)
            serializer = PriceMatrixSerializer(price_matrix, many=True)
            return JsonResponse({"data": serializer.data}, status=200)
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class EventWeekView(generics.GenericAPIView):
    serializer_class = EventWeekSerializer

    def post(self, request):
        # print(request.user)
        instance = EventWeek.objects.all()
        serializer = EventWeekSerializer(
            data=[{"event": 2, "week_number": 0, "Week_start_date": "2021-01-01", "Week_end_date": "2021-01-01"}], many=True)
        # print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return JsonResponse({'message': 'success', 'data': serializer.data}, status=200)


class DayWiseWeekDetailsView(generics.GenericAPIView):
    serializer_class = DayWiseWeekDetailsSerializer

    def post(self, request):
        instance = DayWiseWeekDetails.objects.all()
        serializer = DayWiseWeekDetailsSerializer(data=[{"event_week": 1, "customer": 3, "student": 2, "monday": True, "tuesday": True,
                                                         "wednesday": True, "thursday": True, "friday": True, "saturday": True, "sunday": True, "number_of_days_pass": 0, "cost": 0, "price_matrix": 1}], many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return JsonResponse({'message': 'success', 'data': serializer.data}, status=200)


class OrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        instance = Order.objects.all()
        serializer = OrderSerializer(
            data=[{"event": 1, "customer": 3, "total_cost": 0, "discounted_amount": 0, "order_date": "2021-01-01"}], many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return JsonResponse({'message': 'success', 'data': serializer.data}, status=200)


class OrderSummaryView(generics.GenericAPIView):
    serializer_class = OrderSummarySerializer

    def post(self, request):
        instance = OrderSummary.objects.all()
        serializer = OrderSummarySerializer(
            data=[{"order": 1, "day_wise_week_details": 1, "payment": 1}], many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return JsonResponse({'message': 'success', 'data': serializer.data}, status=200)


class PreschoolBookedDataSaveView(generics.GenericAPIView):

    def post(self, request):

        instance = Order.objects.all()
        serializer = PreschoolBookingPriceFormSubmissionSerializer(
            data=[{"customer": request.data["customer"], "total_cost": request.data["total_cost"]}], many=True)
        print(request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            print("saved")
        else:
            print(serializer.errors)
        return JsonResponse({'message': 'success', 'data': serializer.data}, status=200)


class SaveOrderDetailForCourseView(APIView):

    def post(self, request):
        try:
            with transaction.atomic():
                json_data = request.data
                # print(json_data)



                order_data = json_data['order_details']

                order_serializer = OrderSerializer(data=order_data)

                if order_serializer.is_valid():
                    order_serializer.save()
                else:
                    logger.error(order_serializer.errors,  exc_info=True)
                    # print("order_serializer", order_serializer.errors)
                    return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

                nursery_and_weekly_order_id = []
                for x in json_data['student_order']:
                
                    customer = json_data['customer_id']
                    
                    nursery_and_weekly_student_order_data = {"student": x, "customer": customer}
                    # print(nursery_and_weekly_student_order_data)
                    nursery_and_weekly_student_order_data_serializer = NurseryAndWeeklyStudentOrderDetailsSerializer(data=nursery_and_weekly_student_order_data)
                    if nursery_and_weekly_student_order_data_serializer.is_valid():
                        serializer = nursery_and_weekly_student_order_data_serializer.save()
                        
                        nursery_and_weekly_order_id.append(serializer.id)

                    else:
                        logger.error(nursery_and_weekly_student_order_data_serializer.errors,  exc_info=True)
                        # print("nursery_and_weekly_student_order_data_serializer", nursery_and_weekly_student_order_data_serializer.errors)
                        return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
                # print(nursery_and_weekly_order_id)



                for id in nursery_and_weekly_order_id:

                    
                    payment_reponse = save_payment_data(self, request, json_data)
                    if payment_reponse:
                        json_data['order'] = order_serializer.data["id"]
                        json_data['nursery_and_weekly_student_order_details'] =id
                        json_data['payment'] = payment_reponse['payment']
                        order_summary = json_data

                        order_summary_serializer = OrderSummarySerializer(
                            data=order_summary)

                        if order_summary_serializer.is_valid():
                            order_summary_serializer.save()
                        else:
                            logger.error(order_summary_serializer.errors,  exc_info=True)
                            print("order_summary_serializer", order_summary_serializer.errors)
                            Order.objects.filter(
                                id=order_serializer.data["id"]).delete()
                            Payment.objects.filter(
                                id=payment_reponse['payment']).delete()
                            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
                    else:
                        Order.objects.filter(
                            id=order_serializer.data["id"]).delete()
                        return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

            return JsonResponse({'message': 'success', 'data': payment_reponse['url']}, status=200)

        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class SaveOrderDetailForWeekView(APIView):

    def post(self, request):

        try:
            with transaction.atomic():
                json_data = request.data
                json_data['event'] = json_data.pop(
                    'event_type_id')
                json_data['price_matrix'] = json_data.pop(
                    'price_matrix_id')
                per_week_array = json_data['perWeekArr']
                for per_week in per_week_array:
                    per_week['week_number'] = per_week.pop('weekNumber')
                    per_week['event'] = json_data['event']

                event_week_data = per_week_array
                event_week_serializer = EventWeekSerializer(
                    data=event_week_data, many=True)
 
                if event_week_serializer.is_valid():
                    event_week_serializer.save()
                    event_week_ids = [val['id']
                                      for val in event_week_serializer.data]
                else:
                    logger.error(event_week_serializer.errors,  exc_info=True)
                    return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
                child_arr = []
                for index, per_week in enumerate(per_week_array):
                    for child_array in per_week['childArr']:
                        # print(child_array)
                        child_array['customer'] = json_data['customer']
                        child_array['student'] = child_array.pop(
                            'id')
                        child_array['selection_array'] = child_array.pop(
                            'selectChkArr')
                        child_array['event_week'] = event_week_ids[index]

                        child_arr.append(child_array)

                day_wise_week_data_serializer = DayWiseWeekDetailsSerializer(
                    data=child_arr, many=True)
                # print("day_wise_week", day_wise_week_data_serializer.is_valid())
                if day_wise_week_data_serializer.is_valid():
                    day_wise_week_data_serializer.save()
                    day_wise_week_ids = [val['id']
                                         for val in day_wise_week_data_serializer.data]
                else:
                    logger.error(
                        day_wise_week_data_serializer.errors,  exc_info=True)
                    EventWeek.objects.filter(id__in=event_week_ids).delete()
                    return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

                json_data['event_week'] = event_week_ids
                order_data_serializer = OrderSerializer(data=json_data)
                # print("order data", order_data_serializer.is_valid())
                if order_data_serializer.is_valid():
                    order_data_serializer.save()
                    logger.error(order_data_serializer.data,  exc_info=True)
                else:
                    # print("order_data", order_data_serializer.errors)
                    EventWeek.objects.filter(id__in=event_week_ids).delete()
                    DayWiseWeekDetails.objects.filter(
                        id__in=day_wise_week_ids).delete()
                    return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

                payment_reponse = save_payment_data(self, request, json_data)
                if payment_reponse:
                    json_data['order'] = order_data_serializer.data["id"]
                    # pprint.pprint(json_data['order'])
                    json_data['payment'] = payment_reponse['payment']
                    # pprint.pprint(json_data['payment'])
                    order_summary = json_data

                    order_summary_serializer = OrderSummarySerializer(
                        data=order_summary)
                    # pprint.pprint("order_summary", order_summary_serializer.is_valid())
                    if order_summary_serializer.is_valid():
                        order_summary_serializer.save()
                    else:
                        logger.error(
                            order_summary_serializer.errors, exc_info=True)
                            
                        EventWeek.objects.filter(
                            id__in=event_week_ids).delete()
                        DayWiseWeekDetails.objects.filter(
                            id__in=day_wise_week_ids).delete()
                        Order.objects.filter(
                            id=order_data_serializer.data["id"]).delete()
                        Payment.objects.filter(
                            id=payment_reponse['payment']).delete()
                        return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
                else:
                    EventWeek.objects.filter(id__in=event_week_ids).delete()
                    DayWiseWeekDetails.objects.filter(
                        id__in=day_wise_week_ids).delete()
                    Order.objects.filter(
                        id=order_data_serializer.data["id"]).delete()
                    return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

            return JsonResponse({'message': 'success', 'data': payment_reponse['url']}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)



class StudentWithPaymentDoneView(APIView):

    def get(self, request, pk):
        try:
            order_summary = OrderSummary.objects.filter(payment__customer_id=pk, payment__status = "OK")
            order_summary_serializer = OrderSummaryForStudentPaymentPaid(order_summary, many=True)
            
           

            return JsonResponse(order_summary_serializer.data, status=200,safe=False)
            # print(order_summary_serializer["nursery_and_weekly_student_order_details"])



        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
    

class LocationByCompany(APIView):

    def get(self, request,dk):

        try:
            # location = list(Location.objects.filter(company_id=pk, location_).values("id","location", "address_line_1", "town", "postal_code", "playing_surface__surface").distinct())
            data = Location.objects.filter(company = dk)
            serializer = GetLocationBYCompany(data, many=True)
            return JsonResponse({"company_name": serializer.data}, status=200)
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class PriceMatricDynamicValueSaveView(APIView):
    """To save dynamic values for courses in price matrix model"""
    def post(self, request):
        try:
            
            price_matrix = {"version": request.data["version"], 
            "course_detail": request.data["course_detail"], 
            "single_day": request.data["single_day"], 
            }
            serializer = PriceMatricForDynamicDataSerializer(data = price_matrix)
            if serializer.is_valid():
                serializer.save()
                # print(price_matrixils.id)
               
                return JsonResponse(serializer.data, status=200, safe=False)
            else:
                # print(child.errors)
                return JsonResponse(serializer.data, status=400)
  
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class PriceMatricDynamicValueForHolidaySaveView(APIView):
    """To save dynamic values for courses in price matrix model"""
    def post(self, request):
        try:
            
            price_matrix = {"version": request.data["version"], 
            "course_detail": request.data["course_detail"], 
            "single_day": request.data["single_day"], 
            "two_days": request.data["two_days"],
            "three_days": request.data["three_days"],
            "four_days": request.data["four_days"],
            "five_days": request.data["five_days"],
            }
            serializer = PriceMatricForDynamicDataForHolidaySerializer(data = price_matrix)
            if serializer.is_valid():
                serializer.save()
                # print(price_matrixils.id)
               
                return JsonResponse(serializer.data, status=200, safe=False)
            else:
                # print(child.errors)
                return JsonResponse(serializer.data, status=400)
  
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)