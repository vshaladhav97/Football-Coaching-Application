from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse, Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import CoachSerializer, CoachDataTableSerializer, CoachAnalyticsSerializer, CoachListAnalyticsSerializer
from customer.models import User, Role
from course.models import Events, CourseGroupData
from course.serializer import EventDataSerializer
from .models import Coach, query_coachs_by_args, CoachDocuments
from customer.decorator import check_role_permission
from master.models import AgeGroup
from django.db.models import Count
from first_kick_management.settings import logger
from course.models import (CourseDetail, UserAttendance)
from customer.models import (Student)
from course.serializer import (CourseDetailLocationAnalyticsSerializer,
                               CourseDetailSerializer, CourseDataTableSerializer, CourseGroupDataSerializer)
import datetime
from django.db.models import Q
import json

# Create your views here.


class Error(Exception):
    """Base class for other exceptions"""
    pass


class CoachExistError(Error):
    pass


class CoachListView(generics.GenericAPIView):

    @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/coach_list.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class CoachAddView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt student list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/coach_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

    def post(self, request):
        """
        Create coach
        """
        try:
            coach = Coach.objects.filter(
                email__iexact=request.data['email']).exists()
            if coach:
                raise CoachExistError

            request.data._mutable = False
            coach_serializer = CoachSerializer(data=request.data)
            if coach_serializer.is_valid(
                    raise_exception=True):
                user = User.objects.filter(
                    email__iexact=request.data['email']).exists()
                if not user:
                    user_id = User.objects.create(
                        email=request.data['email'],
                        first_name=request.data['first_name'],
                        last_name=request.data['last_name'],
                        role=Role.objects.get(pk=request.data['role'])
                    )
                    user_id.set_password(request.data['password'])
                    user_id.save()
                user_id = User.objects.get(email__iexact=request.data['email'])
                coach_serializer.validated_data['user'] = user_id
                coach_serializer.validated_data['first_name'] = request.data['first_name']
                coach_serializer.validated_data['last_name'] = request.data['last_name']
                coach_serializer.validated_data['email'] = request.data['email']
                coach_serializer.validated_data['landline'] = request.data['landline']
                coach_serializer.validated_data['address'] = request.data['address']
                coach_serializer.validated_data['town'] = request.data['town']
                coach_serializer.validated_data['postal_code'] = request.data['postal_code']
                coach_serializer.validated_data['profile_image'] = request.data['profile_image']
                # coach_serializer.validated_data['profile_image'] = request.FILES['image']
                coach_serializer.save()

                documents = request.FILES.getlist('documents')

                for i in documents:
                    CoachDocuments.objects.create(
                        coach=Coach.objects.get(
                            email__iexact=request.data['email']),
                        file_path=i
                    )
                return JsonResponse({"message": "coach created successfully"}, status=201)

        except CoachExistError:
            return JsonResponse({'message': "coach already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CoachEditView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request, pk):
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/coach_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class GetAllCoachView(generics.GenericAPIView):
    serializer_class = CoachSerializer

    def get(self, request):
        """
        Get all coachs
        """
        try:
            serializer = CoachSerializer(Coach.objects.all(), many=True)
            return JsonResponse({"message": "list of all coaches", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CoachView(generics.GenericAPIView):
    serializer_class = CoachDataTableSerializer

    def get(self, request):
        """
        Get all caochs
        """
        try:
            datatable_server_processing = query_coachs_by_args(
                request, **request.query_params)
            serializer = CoachDataTableSerializer(
                datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
            # serializer = CoachSerializer(Coach.objects.all(), many=True)
            # return JsonResponse({"message": "coach list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Create coach
        """
        try:
            coach = Coach.objects.filter(
                email__iexact=request.data['email']).exists()
            if coach:
                raise CoachExistError

            request.data._mutable = False
            customer_serializer = CoachSerializer(data=request.data)
            if customer_serializer.is_valid(
                    raise_exception=True):
                user = User.objects.filter(
                    email__iexact=request.data['email']).exists()
                if not user:
                    user_id = User.objects.create(
                        email=request.data['email'],
                        first_name=request.data['first_name'],
                        last_name=request.data['last_name'],
                        role=Role.objects.get(pk=request.data['role']),
                        profile_image=request.FILES['image']
                    )
                    user_id.set_password(request.data['password'])
                    user_id.save()

                user_id = User.objects.get(email__iexact=request.data['email'])
                customer_serializer.validated_data['user'] = user_id
                customer_serializer.validated_data['first_name'] = request.data['first_name']
                customer_serializer.validated_data['last_name'] = request.data['last_name']
                customer_serializer.validated_data['email'] = request.data['email']
                customer_serializer.validated_data['landline'] = request.data['landline']
                customer_serializer.validated_data['address'] = request.data['address']
                customer_serializer.validated_data['town'] = request.data['town']
                customer_serializer.validated_data['postal_code'] = request.data['postal_code']
                customer_serializer.validated_data['profile_image'] = request.FILES['image']
                customer_serializer.save()

                documents = request.FILES.getlist('documents')

                for i in documents:
                    CoachDocuments.objects.create(
                        coach=Coach.objects.get(
                            email__iexact=request.data['email']),
                        file_path=i
                    )

                return JsonResponse({"message": "coach created successfully"}, status=200)

        except CoachExistError:
            return JsonResponse({'message': "coach already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CoachDetailView(generics.GenericAPIView):
    serializer_class = CoachSerializer

    def get_object(self, pk):
        try:
            return Coach.objects.get(pk=pk)
        except Coach.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            coach = self.get_object(pk)
            serializer = CoachSerializer(coach)
            return JsonResponse({'message': 'coach details', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update coach
        """
        try:
            coach = self.get_object(pk)
            print(request.data)
            serializer = CoachSerializer(coach, data=request.data)
            if serializer.is_valid():
                serializer.save()
                documents = request.FILES.getlist('documents')
                for i in documents:
                    CoachDocuments.objects.create(
                        coach=Coach.objects.get(
                            email__iexact=request.data['email']),
                        file_path=i
                    )
                return JsonResponse({'message': 'coach details updated', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete coach
        """
        try:
            coach = self.get_object(pk)
            if coach:
                coach.delete()
                message = "Customer deleted successfully"
                return JsonResponse({'message': message}, status=200)
            return JsonResponse({'message': "coach not found"}, status=401)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class VenueAnalytics(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/venue_analytics.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ClassRegisterView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/class_register.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class RotaView(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'coach/rota.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class RotaDataView(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated,)

    def get(self, request, order_by="start_date"):
        try:
            today = datetime.datetime.now().date()
            week_last_date = today + datetime.timedelta(days=7)
            events = Events.objects.filter(Q(start_date__gte=today) & Q(
                start_date__lte=week_last_date)).annotate(dcount=Count('start_date')).order_by(order_by)
            event_serializer = EventDataSerializer(events, many=True)
            return JsonResponse({'message': 'event details', 'data': event_serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        try:
            course_group = CourseGroupData.objects.get(
                pk=request.data['course_group_id'])

            if course_group.start_time:
                all_course_groups = CourseGroupData.objects.filter(
                    Q(course_detail=CourseDetail.objects.get(pk=request.data['course_id'])) & Q(
                        start_time=course_group.start_time))
                if 'coach1' in request.data:
                    coach = Coach.objects.get(
                        first_name=request.data['coach1'])
                    for groups in all_course_groups:
                        groups.coach1 = coach
                        groups.save()
                if 'coach2' in request.data:
                    coach = Coach.objects.get(
                        first_name=request.data['coach2'])
                    for groups in all_course_groups:
                        groups.coach2 = coach
                        groups.save()

            if course_group.from_pick_up_time:
                all_course_groups = CourseGroupData.objects.filter(
                    Q(course_detail=CourseDetail.objects.get(pk=request.data['course_id'])) & Q(
                        start_time=course_group.from_pick_up_time))
                if 'coach1' in request.data:
                    coach = Coach.objects.get(
                        first_name=request.data['coach1'])
                    for groups in all_course_groups:
                        groups.coach1 = coach
                        groups.save()
                if 'coach2' in request.data:
                    coach = Coach.objects.get(
                        first_name=request.data['coach2'])
                    for groups in all_course_groups:
                        groups.coach2 = coach
                        groups.save()

            return JsonResponse({'message': 'coach updated'}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


def venue_analytics(request):
    login = True if "login" in request.session else False
    return render(request, 'coach/analytics.html', {"login": login})


class testingrota(APIView):

    def get(self, request):
        try:
            course = CourseDetail.objects.all()
            serializer = CourseDetailSerializer(course, many=True)
            # print(serializer.course_group_data)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class VenueAnalyticsCountView(generics.GenericAPIView):

    def get(self, request):
        try:

            total_courses = CourseDetail.objects.filter().count()
            total_attendence = UserAttendance.objects.all().count()
            total_student = Student.objects.all().count()
            total_outstanding_task = CourseDataTableSerializer(CourseDetail.objects.filter(completed="open").count(), many=True)
            courses_unstaffed = CourseDetail.objects.filter(coach__isnull=True).count()
            count_data = [{"total_course":total_courses, "total_attendence": total_attendence , 
                            "total_student": total_student, "courses_unstaffed": courses_unstaffed ,
                            "total_outstanding_task": total_outstanding_task}]
            
            return JsonResponse(count_data, status=200, safe=False)


                
        except Exception as e:
            logger.error(e)
            # print(e)
            return render(request, '404-error-page.html')

class DynamicVenueAnalyticsCountView(generics.GenericAPIView):
    def get(self, request, pk):
        try:
            total_courses = CourseDetail.objects.filter(coach = pk).count()
            total_attendence = UserAttendance.objects.filter(user = pk).count()
            total_student = Student.objects.filter(customer__user = pk).count()
            count_data = [{"total_course":total_courses, "total_attendence": total_attendence , "total_student": total_student}]

            return JsonResponse(count_data, status=200, safe=False)


                
        except Exception as e:
            logger.error(e)
            return render(request, '404-error-page.html')

class CoachAnalyticsListView(generics.GenericAPIView):

    def get(self, request):

        try:
            coach_list = Coach.objects.all()
            # print(coach_list)
            serializer = CoachListAnalyticsSerializer(coach_list, many=True)
            # print(serializer.data)
            filtered_data = []
            coach_list = []
            for i in serializer.data:
                
                if  i['first_name'] not in coach_list:
                   
                    filtered_data.append(i)
                if i['first_name'] not in coach_list:
                    
                    coach_list.append(i['first_name'])
                    

            return JsonResponse(filtered_data, status=200, safe=False)

        except Exception as e:
            logger.error(e)
            # print(e)
            return render(request, '404-error-page.html')

class VenueAnalyticsListView(APIView):

    def get(self, request):

        try:
            venue_list = CourseDetail.objects.all()
            # print(venue_list)
        
            serializer = CourseDetailLocationAnalyticsSerializer(venue_list, many=True)
            # print(serializer.data)
            filtered_data = []
            location_list = []
            for i in serializer.data:
                
                if  i['location'] not in location_list:
                   
                    filtered_data.append(i)
                if i['location'] not in location_list:
                    
                    location_list.append(i['location'])
                    
            
            return JsonResponse(filtered_data, status=200, safe=False)

        except Exception as e:
            logger.error(e)
            # print(e)
            return render(request, '404-error-page.html')
