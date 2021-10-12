from django.core import serializers
from django.shortcuts import render
from rest_framework import generics
from django.http.response import Http404
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ..serializer import (CourseDetailSerializer1, CourseDetailSerializer, CourseLocationSerializer, 
                          CourseDataTableSerializer, CourseListingDataSerializer, CourseGroupDataEditSerializer, 
                          GetCourseTypeWithCourseDetailSerializer, GetCompanySerializer, CourseDetailSerializerForCourseCreation,
                          GetAllCompaniesDataSerializer, CourseDetailDataSerializer, CourseEditSerializer, CourseDetailByLocationSerializer)
from ..models import (CourseDetail, CourseGroupData,
                      Notification,
                      query_course_by_args, )
from master.models import (CourseType,
                           ClassStatus, Location, PlayingSurface, Ages, Company)

from master.serializer import (CourseTypeSerializer)
from coach.models import Coach
from customer.decorator import check_role_permission
import datetime
from first_kick_management.settings import logger
import json

from django.core.serializers import serialize
class CoursesPageView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Get all courses
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'management/course_listing.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ManagementCourseView(generics.GenericAPIView):
    serializer_class = CourseDataTableSerializer

    def get(self, request):
        """
        Get all customers
        """
        try:
            datatable_server_processing = query_course_by_args(request, **request.query_params)
            serializer = CourseDataTableSerializer(datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class GetAllVenuesByStatusOfCompletion(generics.GenericAPIView):
    """Get All Venues"""
    serializer_class = CourseDataTableSerializer

    def get(self, request):
        """
        Get all customers
        """
        try:
            # datatable_server_processing = query_course_by_args(request, **request.query_params)
            serializer = CourseDataTableSerializer(CourseDetail.objects.all(), many=True)
            result = dict()
            result['data'] = serializer.data
            # result['draw'] = datatable_server_processing['draw']
            # result['recordsTotal'] = datatable_server_processing['total']
            # result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)



class ManagementCourseAddView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    @check_role_permission()
    def get(self, request):
        """
        Gwt course list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'management/course_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return render(request, '404-error-page.html')


class ManagementCourseAddDataView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    # serializer_class = CourseDetailSerializer

    def post(self, request):
        # print('course post request called,',request.data)
        """
        Add Course
        """
        try:
            course_detail_serializer = CourseDetailSerializerForCourseCreation(data=request.data)
            request.data._mutable = True
            end_date = datetime.datetime.strptime(request.data['end_date'], '%Y-%m-%d')
            start_date = datetime.datetime.strptime(request.data['start_date'], '%Y-%m-%d')
            data = (end_date - start_date).days
            request.data['execution_duration'] = data
            request.data['start_date'] = start_date.strftime("%Y-%m-%d")
            request.data['end_date'] = end_date.strftime("%Y-%m-%d")
            request.data._mutable = False
            # print(course_detail_serializer.is_valid())
            # print(course_detail_serializer.data)
            if course_detail_serializer.is_valid(
                    raise_exception=True):
                print('inside if')
                course_detail_serializer.validated_data['course_type'] = CourseType.objects.get(
                    pk=request.data['course_type'])
                    # course_detail_serializer.validated_data['course_type'] = CourseType.objects.get(
                    # pk=request.data['course_type'])
                if CourseType.objects.get(pk=request.data['course_type']).course_name == "Holiday Camp":
                    course_detail_serializer.validated_data['no_of_weeks'] = request.data[
                        'select_no_of_weeks_for_holiday']
                elif CourseType.objects.get(pk=request.data['course_type']).course_name == "Evening Development":
                    course_detail_serializer.validated_data['no_of_weeks'] = request.data[
                        'select_no_of_weeks_for_evening_development']
                else:
                    pass
                print('before object')
                course_detail_serializer.validated_data['location'] = Location.objects.get(pk=request.data['location'])
                print('loc')
                course_detail_serializer.validated_data['course_description'] = request.data['course_description']
                print('2')
                course_detail_serializer.validated_data['joining_fee'] = request.data['joining_fee']
                print('3')
                course_detail_serializer.validated_data['no_of_groups'] = request.data['no_of_groups']
                print('4')
                course_detail_serializer.validated_data['single_day'] = request.data['single_day']
                print('5')
                course_detail_serializer.validated_data['two_days'] = request.data['two_days']
                print('6')
                course_detail_serializer.validated_data['three_days'] = request.data['three_days']
                print('7')
                course_detail_serializer.validated_data['four_days'] = request.data['four_days']
                print('8')
                course_detail_serializer.validated_data['five_days'] = request.data['five_days']
                print('9')
                course_detail_serializer.validated_data['street'] = request.data['street']
                print('10')
                course_detail_serializer.validated_data['town'] = request.data['town']
                print('11')
                course_detail_serializer.validated_data['postal_code'] = request.data['postal_code']
                print('12')
                course_detail_serializer.validated_data['playing_surface'] = PlayingSurface.objects.get(
                    pk=request.data['playing_surface_id'])
                print('13')
                # course_detail_serializer.validated_data['playing_surface'] = request.data['playing_surface']
                course_detail_serializer.validated_data['coach'] = Coach.objects.get(pk=request.data['lead_coach'])
                # course_detail_serializer.validated_data['logo'] = request.data['logo']
                # course_detail_serializer.validated_data['event_type'] = EventType.objects.get(pk=request.data['event_type'])
                course_detail_serializer.validated_data['start_date'] = request.data['start_date']
                course_detail_serializer.validated_data['end_date'] = request.data['end_date']
                course_detail_serializer.validated_data['default_course_rate'] = request.data['default_course_rate']
                course_detail_serializer.validated_data['class_status'] = ClassStatus.objects.get(
                    status_name=request.data['status'])
                course_detail_serializer.validated_data['execution_duration'] = request.data['execution_duration']
                course_detail_serializer.validated_data['welcome_message'] = request.data['welcome_message']
                # print('before save')
                course = course_detail_serializer.save()
                course_detail_id = course.id
                print(course_detail_id)

                for i in range(1, int(request.data['no_of_groups'])+1):
                    age_group = 'age_group[{}]'.format(i)
                    # print(age_group)
                    ages = request.POST.getlist(age_group)
                    # print(ages)
                    for age in ages:
                        # print(age)
                        if CourseType.objects.get(pk=request.data['course_type']).course_name == "Holiday Camp":
                            print('inside if of holiday')
                            # print('oliday',request.data['from_drop_off_time[{}]'.format(i)])
                            # Commented this code by Nilesh 

                            CourseGroupData.objects.create(
                                course_detail=course,
                                age=Ages.objects.get(pk=age),
                                from_drop_off_time=request.data['from_drop_off_time[{}]'.format(i)],
                                from_pick_up_time=request.data['from_pick_up_time[{}]'.format(i)],
                                to_drop_off_time=request.data['to_drop_off_time[{}]'.format(i)],
                                to_pick_up_time=request.data['to_pick_up_time[{}]'.format(i)]
                                # maximum_capacity=request.data['maximum_capacity[{}]'.format(i)]
                            )
                        else:
                            CourseGroupData.objects.create(
                                course_detail=course,
                                age=Ages.objects.get(pk=age),
                                start_time=request.data['start_time[{}]'.format(i)],
                                end_time=request.data['end_time[{}]'.format(i)],
                                maximum_capacity=request.data['maximum_capacity[{}]'.format(i)]
                            )
                print('course type',request.data['course_type'])
                print(request.user)
                print(datetime.datetime.now().date())
                Notification.objects.create(
                    message="New course "+CourseType.objects.get(
                        pk=request.data['course_type']).course_name+" added",
                    from_user_id=request.user,
                    created_date=datetime.datetime.now().date()
                )
                # for month in months:
                #     CourseMonths.objects.create(
                #         course_detail=course,
                #         month=Months.objects.get(pk=int(month))
                #     )
                #
                # for i in range(0, len(locations)):
                #     CourseLocation.objects.create(
                #         course_detail=course,
                #         location=Location.objects.get(pk=locations[i]),
                #         coach=Coach.objects.get(pk=coachs[i]),
                #         total_seats=total_seats[i],
                #         available_seats=total_seats[i],
                #     )

                return JsonResponse({"message": "course created successfully", "course_detail_id": course_detail_id}, status=200)

                # courseLocation = CourseLocation.objects.get(location=request.data['location_id'],
                #                                             course_detail=request.data['course'])
                # courseLocation.available_seats -= 1
                # courseLocation.save()
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e,'error')
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ManagementCourseEditView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt course list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'management/course_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

class ManagementBookEditView(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        """
        Gwt course list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'management/booking_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')



class CourseDetailView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses
        """
        try:
            login = True if "login" in request.session else False
            serializer = CourseDetailSerializer1(CourseDetail.objects.all(), many=True)
            return render(request, 'course/course_listing.html', {"login": login, "data": serializer.data})
        except Exception as e:
            logger.error(e, exc_info=True)
            
            return render(request, '404-error-page.html')


class CourseListingDataView(generics.GenericAPIView):
    serializer_class = CourseListingDataSerializer

    def get(self, request):
        """
        Get all courses
        """
        try:
            serializer = CourseListingDataSerializer(
                CourseDetail.objects.filter(class_status=ClassStatus.objects.get(status_name="Published")), many=True)
            return JsonResponse({"message": "list of courses", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class CourseCategoryView(generics.GenericAPIView):
    
    def get(self, request):
        "Get all course category"
        try:
            category = CourseType.objects.all()
            serializer = CourseTypeSerializer(category, many=True)
            return JsonResponse({"message": "list of course categories", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class CourseCategoryDetailView(generics.GenericAPIView):

    serializer_class = CourseTypeSerializer

    def get_object(self, pk):
        try:
            return CourseType.objects.get(pk=pk)
        except CourseType.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Get all courses
        """
        try:
            serializer = CourseTypeSerializer(CourseType.objects.get(pk=pk))
            return JsonResponse({"message": "course_data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CourseDataView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses
        """
        try:
            serializer = CourseDetailSerializer(
                CourseDetail.objects.filter(class_status=ClassStatus.objects.get(status_name="Published")), many=True)
            return JsonResponse({"message": "course list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Get filtered courses
        """
        try:
            serializer = CourseDetailSerializer(CourseDetail.objects.all(), many=True)
            return JsonResponse({"message": "course list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CourseDetailPageView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request, pk):
        """
        Get all courses
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/course_detail.html', {"login": login, "data": pk})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

class CourseAvailableByFilterView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses by venue
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/course_edit_by_location.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

class CheckForMemberForBookingCourseView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses by venue
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/check_for_member_for_booking.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ChildRegistrationForBookingCourseView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses by venue
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/child_registration_for_booking.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ChildSelectionForPayment(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses by venue
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/child_selection_for_payment.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')



class CustomerRegistrationForBookingCourseView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses by venue
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/customer_registration_part1_for_booking.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

class BookingWithWeeks(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get all courses by venue
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/booking_with_weeks.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')




class CourseDetailDataPageView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get_object(self, pk):
        try:
            return CourseDetail.objects.get(pk=pk)
        except CourseDetail.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # print('course edit called' , pk)
        """
        Get all courses
        """
        try:
            # print('course type data',CourseType.objects.filter('Nursery'))
            serializer = CourseDetailDataSerializer(CourseDetail.objects.filter(id=pk), many=True)
            # serializer = GetCourseTypeWithCourseDetailSerializer(CourseType.objects.filter(id=pk), many=True)
            # print('serilizer data',serializer.data)
            return JsonResponse({"data": serializer.data[0]}, status=200)
        except Exception as e:
            print(e,'error')
            logger.error(e, exc_info=True)
            # print(e)
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


class CourseDetailDataByLocation(generics.GenericAPIView):

    def get(self, request, pk, dk):
        try:
            course_detail = CourseDetail.objects.filter(location =pk, course_type=dk)
            serializer = CourseDetailByLocationSerializer(course_detail, many = True)
            print(serializer.data)
            if len(serializer.data) ==0:
                return JsonResponse({"message": "no data found"}, status = 200, safe=False)
            return JsonResponse(serializer.data, status = 200, safe=False)
        except Exception as e:
            
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)





class CourseCartView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request):
        """
        Get courses based on location
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/cart.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

    # def post(self, request):

    #     try:
    #         serializer = CourseGroupDataSerializer(
    #             CourseGroupData.objects.get(course_detail=request.data['course_id']))

    #         return JsonResponse({"message": "course data", "data": serializer.data}, status=200)
    #     except Exception as e:
    #         logger.error(e, exc_info=True)
    #         return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class FilteredCoursesView(generics.GenericAPIView):
    serializer_class = CourseDetailSerializer

    def get(self, request, pk, id):
        """
        Get courses based on location
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'course/filtered_courses.html', {"login": login, "data": pk, "age_group": id})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class FilteredCourseDataView(generics.GenericAPIView):
    serializer_class = CourseLocationSerializer

    def get(self, request, pk, id, month):
        """
        Get courses through location
        """
        try:
            serializer = CourseDetailSerializer(
                CourseDetail.objects.filter(
                    Q(location=pk) & Q(pk=id) & Q(start_date__month__lte=month)
                    & Q(end_date__month__gte=month)), many=True)
            return JsonResponse({"message": "course data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ApproveCourseView(generics.GenericAPIView):
    def post(self, request, pk):
        """
        Update course as published
        """
        try:
            course_detail = CourseDetail.objects.get(pk=pk)
            course_detail.class_status = ClassStatus.objects.get(
                    status_name="Published")
            course_detail.save()
            return JsonResponse({"message": "course published"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class test_rota(generics.GenericAPIView):

    def get(self, request):

        try:
            rota = CourseGroupData.objects.all()
            serializer = CourseGroupDataEditSerializer(rota ,many=True)
            return JsonResponse(serializer.data, safe=False)
        
        except Exception as e:
            logger.error(e, exc_info=True)
        
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class GetLocation(generics.GenericAPIView):
    # serializer_class = MonthSerializer

    def get(self, request, pk):
        """
        Get all weekdays
        """
        try:
            
            # serializer = MonthSerializer(Months.objects.all(), many=True)
            data = list(CourseDetail.objects.filter(course_type__id=pk).values("location", "location__location", "location__address_line_1", "location__town", "location__postal_code", "location__playing_surface__surface",))

            

           
            return JsonResponse({"company_name": data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class GetCompany(generics.GenericAPIView):
    # serializer_class = MonthSerializer

    def get(self, request, pk):
        """
        Get all weekdays
        """
        try:
            # print(pk)
            # serializer = MonthSerializer(Months.objects.all(), many=True)
            data = list(CourseDetail.objects.filter(course_type__id=pk).values("location__company__id","location__company__company_name").distinct())
            # print(data)
            
            # return JsonResponse(serialize("json", data), status=200, safe=False)
            return JsonResponse({"company_name": data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class AllCompanyNamesViews(generics.GenericAPIView):
    # serializer_class = MonthSerializer

    def get(self, request):
        """
        Get all weekdays
        """
        try:
            # print(pk)
            # serializer = MonthSerializer(Months.objects.all(), many=True)
            data = Company.objects.all()
            serializer = GetAllCompaniesDataSerializer(data, many=True)
            # print(data)
            
            # return JsonResponse(serialize("json", data), status=200, safe=False)
            return JsonResponse({"company_name": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class GetCompaniesForDropdown(generics.GenericAPIView):


    def get(self, request, pk):
        """
        Get all weekdays
        """
        try:
            course_details = Location.objects.filter(pk=pk)
            serializer = GetCompanySerializer(course_details, many=True)
            return JsonResponse({"company_name": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class TestClassGroupData(generics.GenericAPIView):

    def get(self,request):
        try:
            course_group = CourseDetail.objects.all()
            serializers = CourseDetailSerializer(course_group, many=True)
            return JsonResponse({"company_name": serializers.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class CourseEditFunctionalityView(generics.GenericAPIView):
    """Course Edit Functionality view"""

    # def get_object(self, pk):
    #     try:
    #         return CourseDetail.objects.get(pk=pk)
    #     except CourseDetail.DoesNotExist:
    #         raise Http404

    def put(self, request, pk):

        try:
            course_detail = CourseDetail.objects.get(id = pk)
            # print(course_detail)
            serializer = CourseEditSerializer(course_detail , data=request.data)
            request.data._mutable = True
            end_date = datetime.datetime.strptime(request.data['end_date'], '%Y-%m-%d')
            start_date = datetime.datetime.strptime(request.data['start_date'], '%Y-%m-%d')
            request.data['start_date'] = start_date.strftime("%Y-%m-%d")
            # print('sdate',request.data['start_date'] )
            request.data['end_date'] = end_date.strftime("%Y-%m-%d")
            # print('edate',request.data['end_date'] )
            data = (end_date - start_date).days
            request.data['execution_duration'] = data
            request.data._mutable = False
            # print(serializer.is_valid())
            # if serializer.is_valid():
            if serializer.is_valid(
                    raise_exception=True):

                serializer.validated_data['course_type_id'] = request.data['course_type']
                serializer.validated_data['logo'] = request.data['logo']
                serializer.validated_data['start_date'] = request.data['start_date']
                serializer.validated_data['end_date'] = request.data['end_date']
                serializer.validated_data['default_course_rate'] = request.data['default_course_rate']
                serializer.validated_data['course_description'] = request.data['course_description']
                serializer.validated_data['event_type_id'] = request.data['event_type']
                serializer.validated_data['class_status_id'] = request.data['class_status']

                serializer.save()
                return JsonResponse(serializer.data , status=200)
            
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)