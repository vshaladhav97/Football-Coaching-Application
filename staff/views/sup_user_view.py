from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse, Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializer import StaffSerializer, StaffDataTableSerializer
from customer.serializer import UserSerializer
from customer.models import User, Role, query_super_users_by_args
from customer.decorator import check_role_permission
from master.models import AgeGroup
from first_kick_management.settings import logger

# Create your views here.


class Error(Exception):
    """Base class for other exceptions"""
    pass


class SuperUserExistError(Error):
    pass


class SuperUserListView(generics.GenericAPIView):

    # @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'staff/sup_user_list.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class SuperUserAddView(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        """
        Gwt super user list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'staff/sup_user_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

    def post(self, request):
        """
        Create super user
        """
        try:
            user = User.objects.filter(email__iexact=request.data['email']).exists()
            if user:
                raise SuperUserExistError

            if not user:
                user_id = User.objects.create(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    role=Role.objects.get(name__iexact="Super User")
                )
                user_id.set_password(request.data['password'])
                user_id.save()
                return JsonResponse({"message": "created successfully"}, status=200)

        except SuperUserExistError:
            return JsonResponse({'message': "super user already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class SuperUserEditView(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request, pk):
        try:
            login = True if "login" in request.session else False
            return render(request, 'staff/sup_user_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class GetAllSuperUserView(generics.GenericAPIView):
    serializer_class = StaffSerializer

    def get(self, request):
        """
        Get all super users
        """
        try:
            serializer = UserSerializer(User.objects.filter(
                role=Role.objects.get(name__iexact="Super User")), many=True)
            return JsonResponse({"message": "fetch all super users", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class SuperUserView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        """
        Get all staff users
        """
        try:
            datatable_server_processing = query_super_users_by_args(request, **request.query_params)
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
            user = User.objects.filter(email__iexact=request.data['email']).exists()
            if user:
                raise SuperUserExistError

            if not user:
                user_id = User.objects.create(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    role=Role.objects.get(name__iexact="Super User"),
                    profile_image=request.FILES['image']
                )
                user_id.set_password(request.data['password'])
                user_id.save()

                return JsonResponse({"message": "created successfully"}, status=200)

        except SuperUserExistError:
            return JsonResponse({'message': "super user already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class SuperUserDetailView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            return JsonResponse({'message': 'get super user detail', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update super user
        """
        try:
            userData = User.objects.get(pk=pk)
            # userData.email = request.data['email'],

            userData.last_name = request.data['last_name']
            userData.save()
            return JsonResponse({'message': 'super user details updated'}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete user
        """
        try:
            user = self.get_object(pk)
            if user:
                user.delete()
                return JsonResponse({'message': "super user deleted successfully"}, status=200)
            return JsonResponse({'message': "super user not found"}, status=401)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


