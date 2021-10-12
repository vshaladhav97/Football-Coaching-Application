from django.shortcuts import render
from rest_framework import generics
from django.http.response import Http404
from django.http.response import JsonResponse
from rest_framework.response import Response
from ..serializer import (CustomerSerializer, StudentSerializer,CustomerDataSerializer, RoleSerializer,
                         UserSerializer, UserDataSerializer, UserDataTableSerializer, StudentDataTableSerializer,
                         CustomerIdSerializer, StudentDetailsByCustomerSerializer)
from ..models import Customer, User, Student, Role, query_users_by_args, query_students_by_args, CustomerDocuments
from customer.decorator import check_role_permission
from actstream import action
from first_kick_management.settings import logger
from django.db.models import Q

def get_permissions_wit_login(user_id=None):
    """Get Permissons of user"""

    try:
        permissions = User.objects.filter(
            id=user_id
        ).filter(
            role__role_status=True
        ).filter(
            role__permissions__status=True
        ).values(
            'role__permissions__permission_name',
            'role__permissions__api_method',
            'role__permissions__url_identifier')

        # Permissions setting in session
        perms_list_font_end = []
        permission_list_backend = []

        for perm in permissions:
            permission_dict = {}
            for key, value in perm.items():
                if key == 'role__permissions__permission_name':
                    permission_dict['permission_name'] = value.lower()

                elif key == 'role__permissions__api_method':
                    permission_dict['api_method'] = value.lower()

                else:
                    permission_dict['url_identifier'] = value

            perm_name_method = perm['role__permissions__permission_name'].lower(
            ) + '_' + perm['role__permissions__api_method'].lower()
            perms_list_font_end.append(perm_name_method)
            permission_list_backend.append(permission_dict)

        return perms_list_font_end

    except Exception as e:
        info_message = "Permission fetching  issue due to Internal Server Error"
        logger.error(e, exc_info=True)
        return info_message


class Error(Exception):
    """Base class for other exceptions"""
    pass


class CustomerExistError(Error):
    pass


class CustomerListView(generics.GenericAPIView):

    @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'user/user_list.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

            


class CustomerAddView(generics.GenericAPIView):

    @check_role_permission()
    def get(self, request):
        """
        Gwt customer add view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'user/user_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class CustomerEditView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request, pk):
        try:
            login = True if "login" in request.session else False
            return render(request, 'user/user_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class CustomerView(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    def get(self, request):
        """
        Get all customers
        """
        datatable_server_processing = query_users_by_args(request, **request.query_params)
        serializer = UserDataTableSerializer(datatable_server_processing['items'], many=True)
        result = dict()
        result['data'] = serializer.data
        result['draw'] = datatable_server_processing['draw']
        result['recordsTotal'] = datatable_server_processing['total']
        result['recordsFiltered'] = datatable_server_processing['count']
        return Response(result)

    def post(self, request):
        """
        Create customer
        """
        try:
            customer = Customer.objects.filter(email__iexact=request.data['email']).exists()
            if customer:
                raise CustomerExistError

            customer_serializer = CustomerSerializer(data=request.data)
            # print(customer_serializer.data)
            # print(customer_serializer.is_valid())
            if customer_serializer.is_valid(
                    raise_exception=True):
                user = User.objects.filter(email__iexact=request.data['email']).exists()
                if not user:
                    user_id = User.objects.create(
                        email=request.data['email'],
                        first_name=request.data['first_name'],
                        last_name=request.data['last_name'],
                        role=Role.objects.get(name__iexact="Customer")
                    )
                    user_id.set_password(request.data['password'])
                    user_id.save()
                user_id = User.objects.get(email__iexact=request.data['email'])
                customer_serializer.validated_data['user'] = user_id
                customer_serializer.validated_data['first_name'] = request.data['first_name']
                customer_serializer.validated_data['last_name'] = request.data['last_name']
                customer_serializer.validated_data['email'] = request.data['email']
                customer_serializer.validated_data['landline'] = request.data['landline']
                # customer_serializer.validated_data['town'] = request.data['town']
                customer_serializer.validated_data['address'] = request.data['address']
                customer_serializer.validated_data['postal_code'] = request.data['postal_code']
                customer_serializer.validated_data['country_code'] = request.data['country_code']
                
                customer_serializer.validated_data['profile_image'] = request.FILES['image']
                customer = customer_serializer.save()
                # print(customer.id)

                documents = request.FILES.getlist('documents')

                action.send(customer, verb="New customer" + customer.first_name + "added")

                for i in documents:
                    CustomerDocuments.objects.create(
                        customer=Customer.objects.get(email__iexact=request.data['email']),
                        file_path=i
                    )

                return JsonResponse({"message": "customer created successfully", "customer_id": customer.id}, status=200)

        except CustomerExistError:
            return JsonResponse({'message': "customer already exist"})

        except Exception as e:
            print(e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CustomerDetailView(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            customer = self.get_object(pk)
            serializer = CustomerSerializer(customer)
            return JsonResponse({'message': 'list of all customers', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update customer
        """
        try:
            customer = self.get_object(pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                documents = request.FILES.getlist('documents')
                for i in documents:
                    CustomerDocuments.objects.create(
                        customer=Customer.objects.get(email__iexact=request.data['email']),
                        file_path=i
                    )
                return JsonResponse({'message': 'customer details updated', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete buyer
        """
        try:
            customer = self.get_object(pk)
            if customer:
                action.send(customer, verb="Customer with name " + customer.first_name + "has been deleted")
                customer.delete()
                message = "Customer deleted successfully"
                return JsonResponse({'message': message}, status=200)
            return JsonResponse({'message': "Customer not found"}, status=401)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CustomerRegistrationView(generics.GenericAPIView):

    @check_role_permission()
    def get(self, request):
        """
        Get login page
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'customer_registration.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class GetAllCustomers(generics.GenericAPIView):
    def get(self, request):
        """
        Get all customers
        """
        try:
            serializer = CustomerDataSerializer(Customer.objects.all(), many=True)
            return JsonResponse({'message': 'fetch all customers', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class RolesView(generics.GenericAPIView):
    def get(self, request):
        """
        Get all roles
        """
        try:
            serializer = RoleSerializer(Role.objects.all(), many=True)
            return JsonResponse({'message': 'fetch all roles', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class RoleForCoachView(generics.GenericAPIView):
    def get(self, request):
        """
        Get all roles
        """
        try:
            serializer = RoleSerializer(Role.objects.filter(Q(name="Coach Manager") | Q(name="Head Coach")  | Q(name="Assisting Coach")), many=True)
            return JsonResponse({'message': 'fetch all roles', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CustomerId(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            customer_id = Customer.objects.filter(email=pk)
            serializer = CustomerIdSerializer(customer_id, many=True)
            return JsonResponse({'message': 'fetch all roles', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class StudentDetailsByCustomer(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            student = Student.objects.filter(customer=pk)
            serializer = StudentDetailsByCustomerSerializer(student, many=True)
            return JsonResponse({'message': 'fetch all roles', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)