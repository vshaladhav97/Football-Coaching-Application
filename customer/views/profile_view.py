import json
from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from staff.models import Staff
from coach.serializer import CoachSerializer, CoachUserSerializer
from staff.serializer import StaffSerializer, StaffUserSerializer
from ..serializer import (CustomerSerializer, StudentSerializer,CustomerDataSerializer, CustomerUserSerializer,
                         UserSerializer, UserDataSerializer, UserDataTableSerializer, StudentDataTableSerializer,
                          CustomerRegistrationSerializer, StudentSerializer, CustomerIdForBookingSerializer)
from ..models import Customer, User, Student, Role, query_users_by_args, query_students_by_args, CustomerDocuments
from coach.models import Coach, CoachDocuments
from customer.decorator import check_role_permission
from first_kick_management.settings import logger



class UpdateRolePageView(generics.GenericAPIView):
    def get(self, request):
        """
        Gwt student list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'role.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class UpdateRoleView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = User.objects.filter(email__iexact=request.user).exists()
            if user:
                user = User.objects.get(email__iexact=request.user)
                user.role = Role.objects.get(name__iexact=request.data['role'])
                user.save()

                # print(request.data['role'], "ROLE")
                if request.data['role'] == "Customer":
                    Customer.objects.create(
                        user=user,
                        email=user.email
                    )

                if request.data['role'] == "Coach":
                    Coach.objects.create(
                        user=user,
                        email=user.email
                    )

            return JsonResponse({'message': "role updated"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ProfileView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt profile view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'profile.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ProfileDataView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        get profile data
        """
        try:
            if request.user.role.name == "Customer":
                serializer = CustomerUserSerializer(Customer.objects.get(email=request.user.email))
            elif request.user.role.name in ["Coach Manager", "Head Coach"]:
               
                serializer = CoachUserSerializer(Coach.objects.get(email=request.user.email))
            elif request.user.role.name == "Management":
                serializer = StaffUserSerializer(Staff.objects.get(email=request.user.email))
            else:
                serializer = UserSerializer(User.objects.get(pk=request.user.id))
            return JsonResponse({"message": "user data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Update user data
        """
        try:
            user_id = User.objects.get(pk=request.data['user_id'])
            user_id.first_name = request.data['first_name']
            user_id.last_name = request.data['last_name']
            role = request.user.role.name
            image = request.data['image']
            if image:
                user_id.avatar = request.FILES['image']
                if role == "Customer":
                    customer = Customer.objects.get(email=user_id.email)
                    customer.first_name = request.data['first_name']
                    customer.last_name = request.data['last_name']
                    customer.mobile = request.data['mobile']
                    customer.landline = request.data['landline']
                    customer.postal_code = request.data['post_code']
                    customer.address = request.data['address']
                    customer.profile_image = request.FILES['image']
                    customer.save()

                elif role in ["Coach Manager", "Head Coach"]:
                    coach = Coach.objects.get(email=user_id.email)
                    coach.first_name = request.data['first_name']
                    coach.last_name = request.data['last_name']
                    coach.mobile = request.data['mobile']
                    coach.landline = request.data['landline']
                    coach.postal_code = request.data['post_code']
                    coach.address = request.data['address']
                    coach.profile_image = request.FILES['image']
                    coach.save()

                    documents = request.FILES.getlist('documents')

                    for i in documents:
                        CoachDocuments.objects.create(
                            coach=Coach.objects.get(email__iexact=request.data['email']),
                            file_path=i
                        )

                elif role == "Management":
                    staff = Staff.objects.get(email=user_id.email)
                    staff.first_name = request.data['first_name']
                    staff.last_name = request.data['last_name']
                    staff.mobile = request.data['mobile']
                    staff.landline = request.data['landline']
                    staff.postal_code = request.data['post_code']
                    staff.address = request.data['address']
                    staff.save()
                else:
                    pass
            if request.POST.get('password'):
                user_id.set_password(request.data['password'])
            user_id.save()
            return JsonResponse({"message": "user data"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)





class UserView(generics.GenericAPIView):
    def get(self, request):
        """
        Get all users
        """
        try:
            serializer = UserDataSerializer(User.objects.filter(role__isnull=False), many=True)
            return JsonResponse({'message': 'list of users', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)



class RegistrationPart1(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        """
        Gwt profile view
        """
        try:
            # print(request.session["login"])
            login = True if "login" in request.session else False
            return render(request, 'course/customer_reg_part1.html', {"login": login})

        
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

class RegistrationPart2(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        """
        Gwt profile view
        """
        try:
            # print(request.session["login"])
            login = True if "login" in request.session else False
            return render(request, 'course/customer_reg_part2.html', {"login": login})

        
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

class OrderSummaryForPreschool(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        """
        order summary for preschool
        """
        try:
            # print(request.session["login"])
            login = True if "login" in request.session else False
            return render(request, 'course/order_summary_preschool.html', {"login": login})

        
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')



class RegistrationDataView(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        get profile data
        """
        try:
            if request.user.role.name == "Customer":
                serializer = CustomerSerializer(Customer.objects.get(email=request.user.email))
            elif request.user.role.name in ["Coach Manager", "Head Coach"]:
                # print("dDDDDD")
                serializer = CoachUserSerializer(Coach.objects.get(email=request.user.email))
            elif request.user.role.name == "Management":
                serializer = StaffUserSerializer(Staff.objects.get(email=request.user.email))
            else:
                serializer = UserSerializer(User.objects.get(pk=request.user.id))
            return JsonResponse({"message": "user data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Update user data
        """
        try:

            # user_id = User.objects.get(pk=request.data['user_id'])
  
            # user_id = 1
            json_data = request.data
            customer_data = {"user": 1, "first_name": request.data["first_name"], "last_name": request.data["last_name"], "email": request.data["email"],
                "mobile": request.data["mobile"], "landline": request.data["landline"], "postal_code": request.data["postal_code"],
                "country_code": request.data["country_code"], "address": request.data["address"]}
            # print(request.data)
            customer = CustomerRegistrationSerializer(data=customer_data)
            # print(customer.is_valid())
            if customer.is_valid():
                customer.save()
                # print(customer)
                customer["id"].value
                return JsonResponse(customer["id"].value, status=200, safe=False)
            else:
                print(customer.errors)
                return JsonResponse(customer.data, status=400)
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)



class ChildRegistration(generics.GenericAPIView):


    def post(self, request):
        
        try: 
            json_data = request.data
            # print(json_data)
            # print(type(request.data["customer_id"]))
            # customer = Customer.objects.get(id=json_data['customer_id'])
            child_data = {"first_name": request.data["first_name"], "last_name": request.data["last_name"], "birthdate": request.data["birthdate"], "medical_issue":request.data["medical_issue"], "ages": request.data["age_group"], "customer": request.data["customer_id"]}
            # print(request.data)
            child = StudentSerializer(data=child_data)
            # print(child.is_valid())
            if child.is_valid():
                child_datails = child.save()
                # print(child_datails.id)
                child_data['student_id'] = child_datails.id
                return JsonResponse(child_data, status=200, safe=False)
            else:
                # print(child.errors)
                return JsonResponse(child.data, status=400)
        except Exception as e:
            
            logger.error(e, exc_info=True)
            # print("error", e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class CustomerListForBooking(generics.GenericAPIView):

    def get(self, request):
        try:
            customer = Customer.objects.order_by('-id')[0:1]
            serializer = CustomerIdForBookingSerializer(customer, many=True)
            return JsonResponse({"message": "customer data", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

        
