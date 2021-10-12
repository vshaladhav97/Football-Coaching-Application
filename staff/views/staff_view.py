from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse, Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializer import StaffSerializer, StaffDataTableSerializer
from customer.models import User, Role
from ..models import Staff, query_staffs_by_args
from customer.decorator import check_role_permission
from master.models import AgeGroup
from first_kick_management.settings import logger

# Create your views here.


class Error(Exception):
    """Base class for other exceptions"""
    pass


class StaffExistError(Error):
    pass


class StaffListView(generics.GenericAPIView):

    # @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'staff/staff_list.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class StaffAddView(generics.GenericAPIView):
    def get(self, request):
        """
        Gwt staff list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'staff/staff_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

    def post(self, request):
        """
        Create staff
        """
        try:
            staff = Staff.objects.filter(email__iexact=request.data['email']).exists()
            if staff:
                raise StaffExistError
            request.data._mutable = False
            staff_serializer = StaffSerializer(data=request.data)
            if staff_serializer.is_valid(
                    raise_exception=True):
                user = User.objects.filter(email__iexact=request.data['email']).exists()
                if not user:
                    user_id = User.objects.create(
                        email=request.data['email'],
                        first_name=request.data['first_name'],
                        last_name=request.data['last_name'],
                        role=Role.objects.get(name__iexact="Management")
                    )
                    user_id.set_password(request.data['password'])
                    user_id.save()
                user_id = User.objects.get(email__iexact=request.data['email'])
                staff_serializer.validated_data['user'] = user_id
                staff_serializer.validated_data['first_name'] = request.data['first_name']
                staff_serializer.validated_data['last_name'] = request.data['last_name']
                staff_serializer.validated_data['email'] = request.data['email']
                staff_serializer.validated_data['landline'] = request.data['landline']
                staff_serializer.validated_data['address'] = request.data['address']
                staff_serializer.validated_data['postal_code'] = request.data['postal_code']
                staff_serializer.save()

                return JsonResponse({"message": "created successfully"}, status=200)

        except StaffExistError:
            return JsonResponse({'message': "staff already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class StaffEditView(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request, pk):
        try:
            login = True if "login" in request.session else False
            return render(request, 'staff/staff_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class GetAllStaffView(generics.GenericAPIView):
    serializer_class = StaffSerializer

    def get(self, request):
        """
        Get all staff users
        """
        try:
            serializer = StaffSerializer(Staff.objects.all(), many=True)
            return JsonResponse({"message": "fetch all staffs", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class StaffView(generics.GenericAPIView):
    serializer_class = StaffDataTableSerializer

    def get(self, request):
        """
        Get all staff users
        """
        try:
            datatable_server_processing = query_staffs_by_args(request, **request.query_params)
            serializer = StaffDataTableSerializer(datatable_server_processing['items'], many=True)
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
        Create staff
        """
        try:
            staff = Staff.objects.filter(email__iexact=request.data['email']).exists()
            if staff:
                raise StaffExistError

            request.data._mutable = False
            staff_serializer = StaffSerializer(data=request.data)
            if staff_serializer.is_valid(
                    raise_exception=True):
                user = User.objects.filter(email__iexact=request.data['email']).exists()
                if not user:
                    user_id = User.objects.create(
                        email=request.data['email'],
                        first_name=request.data['first_name'],
                        last_name=request.data['last_name'],
                        role=Role.objects.get(name__iexact="Management"),
                        profile_image=request.FILES['image']
                    )
                    user_id.set_password(request.data['password'])
                    user_id.save()

                user_id = User.objects.get(email__iexact=request.data['email'])
                staff_serializer.validated_data['user'] = user_id
                staff_serializer.validated_data['first_name'] = request.data['first_name']
                staff_serializer.validated_data['last_name'] = request.data['last_name']
                staff_serializer.validated_data['email'] = request.data['email']
                staff_serializer.validated_data['landline'] = request.data['landline']
                staff_serializer.validated_data['address'] = request.data['address']
                staff_serializer.validated_data['postal_code'] = request.data['postal_code']
                staff_serializer.validated_data['profile_image'] = request.FILES['image']
                staff_serializer.save()

                return JsonResponse({"message": "created successfully"}, status=200)

        except StaffExistError:
            return JsonResponse({'message': "staff already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class StaffDetailView(generics.GenericAPIView):
    serializer_class = StaffSerializer

    def get_object(self, pk):
        try:
            return Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            staff = self.get_object(pk)
            serializer = StaffSerializer(staff)
            return JsonResponse({'message': 'get staff detail', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update staff
        """
        try:
            staff = self.get_object(pk)
            serializer = StaffSerializer(staff, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'staff details updated', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete staff
        """
        try:
            staff = self.get_object(pk)
            if staff:
                staff.delete()
                return JsonResponse({'message': "staff deleted successfully"}, status=200)
            return JsonResponse({'message': "staff not found"}, status=401)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


