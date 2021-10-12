from django.shortcuts import render
from rest_framework import generics
from django.http.response import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializer import (CustomerSerializer, StudentSerializer, CustomerDataSerializer,
                          UserSerializer, UserDataSerializer, UserDataTableSerializer, StudentDataTableSerializer,
                          ChildEditSerialier, CourseGroupDataForStudentSerializer, AgeSerializer, ChildEditSerialierData,
                          ChildGetPrepopulateSerialierData)
from course.serializer import (BookCourseDetailSerializer, EventSerializer)
from ..models import Customer, User, Student, Role, query_users_by_args, query_students_by_args, CustomerDocuments
from course.models import CourseDetail, CartItem, Cart, Events, CourseGroupData
from master.models import AgeGroup, Location, Ages
from customer.decorator import check_role_permission
from actstream import action
from django.db.models import F
from first_kick_management.settings import logger
from django.db.models import Count
import datetime
# import pprint


class StudentListView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt student list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'student/student_list.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class StudentAddView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        """
        Gwt student add view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'student/student_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class StudentEditView(generics.GenericAPIView):
    # @check_role_permission()
    def get(self, request):
        """
        Gwt student edit view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'student/student_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class StudentView(generics.GenericAPIView):
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def createEvents(self, student, course_detail, step, title):
        start = course_detail.start_date
        end = course_detail.end_date
        step = datetime.timedelta(days=step)
        while start <= end:
            Events.objects.create(
                student=student,
                course_detail=course_detail,
                start_date=start,
                end_date=start,
                title=title
            )
            start += step
        return True

    def get(self, request):
        """
        Get all students
        """
        try:
            datatable_server_processing = query_students_by_args(
                request, **request.query_params)
            serializer = StudentDataTableSerializer(
                datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
        # try:
        #     serializer = StudentSerializer(Student.objects.filter(customer=Customer.objects.get(email=request.user)), many=True)
        #     return JsonResponse({"message": "student list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Create student
        """
        try:
            student_serializer = StudentSerializer(data=request.data)
            if student_serializer.is_valid(
                    raise_exception=True):
                customer = Customer.objects.filter(
                    email__iexact=request.user).exists()
                if customer:
                    customer = Customer.objects.get(email__iexact=request.user)
                else:
                    # user = User.objects.get(pk=request.data['customer_id'])
                    customer = Customer.objects.get(
                        pk=request.data['customer_id'])
                age_group = AgeGroup.objects.get(pk=request.data['age-group'])
                student_serializer.validated_data['customer'] = customer
                student_serializer.validated_data['first_name'] = request.data['first_name']
                student_serializer.validated_data['last_name'] = request.data['last_name']
                student_serializer.validated_data['age'] = request.data['age']
                student_serializer.validated_data['age_group'] = age_group
                student_serializer.validated_data['school_name'] = request.data['school_name']
                student = student_serializer.save()

                course_detail = CourseDetail.objects.get(
                    pk=request.data['course'])

                if request.user.role == "Customer":
                    cart = Cart.objects.get(created_by=request.user)
                    cart_items = CartItem.objects.get(
                        cart=cart, purchased=True, course=course_detail, purchased_qty__gt=F('booked_qty'))
                    cart_items.booked_qty += 1
                    cart_items.save()

                # end_date = datetime.datetime.strptime(request.data['end_date'], '%Y-%m-%d')
                # start_date = datetime.datetime.strptime(request.data['start_date'], '%Y-%m-%d')
                request.data._mutable = True
                request.data['end_date'] = course_detail.end_date
                request.data['start_date'] = course_detail.start_date
                request.data['student'] = student.pk
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
                    course_booked_for_student = book_course_seriliazer.save()

                if course_detail.course_type.course_name == "Evening Development":
                    self.createEvents(student, course_detail,
                                      step=7, title="Evening Development")

                    action.send(request.user,
                                verb=request.user.first_name + " has booked for the student " + request.data['first_name'])

                return JsonResponse({"message": "created successfully"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class GetAlStudentView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            role = str(request.user.role)
            if role == "Customer":
                customer = Customer.objects.get(
                    email__iexact=request.user.email)
                serializer = StudentSerializer(
                    Student.objects.filter(customer=customer), many=True)
            else:
                serializer = StudentSerializer(
                    Student.objects.all(), many=True)

            return JsonResponse({'message': 'get students', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class StudentDetailView(generics.GenericAPIView):
    serializer_class = StudentSerializer

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            student = self.get_object(pk)
            serializer = StudentSerializer(student)
            return JsonResponse({'message': 'get student details', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update student
        """
        try:
            student = self.get_object(pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                age_group = AgeGroup.objects.get(pk=request.data['age-group'])
                serializer.validated_data['age_group'] = age_group
                serializer.save()
                return JsonResponse({'message': 'get age groups', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete buyer
        """
        try:
            student = self.get_object(pk)

            if student:
                student.delete()
                return JsonResponse({'message': "Student deleted successfully"}, status=200)
            return JsonResponse({'message': "Customer not found"}, status=401)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ClassRegister(generics.GenericAPIView):
    def get(self, request):
        """
        Delete buyer
        """
        try:
            date = datetime.datetime.date()
            serializer = EventSerializer(
                Events.objects.filter(start_date=date), many=True)
            return JsonResponse({'message': 'students list', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ChildsList(generics.GenericAPIView):
   # @check_role_permission()
    def get(self, request):
        """
        child profile view
        """
        try:
            # print(request.session["login"])
            login = True if "login" in request.session else False
            return render(request, 'student/child_list.html', {"login": login})

        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class ChildEditView(generics.GenericAPIView):

    def get(self, request):
        try:
            child = Student.objects.all()
            serializers = ChildEditSerialier(child, many=True)
            # print(serializers.data)
            return JsonResponse(serializers.data, safe=False)
        except Exception as e:
            # print("error", e)
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

    def put(self, request):

        try:
            child = Student.objects.get(id=request.data["child_id"])

            serializer = ChildEditSerialier(child, data=request.data)

            if serializer.is_valid():
                # print("in if loop")
                # age_group = AgeGroup.objects.get(pk=request.data['age-group'])
                serializer.validated_data['first_name'] = request.data["first_name"]
                serializer.validated_data['last_name'] = request.data["last_name"]
                serializer.validated_data['birthdate'] = request.data["birthdate"]
                serializer.validated_data['medical_issue'] = request.data["medical_issue"]
                serializer.save()
            return JsonResponse({"message": "success"}, status=200)
        except Exception as e:
            # print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class AllStudentDetails(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            child = Student.objects.filter(id=pk)
            serializer = ChildGetPrepopulateSerialierData(child, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request):
        print("formdata", request.data)
        try:
            # print(request.data["id"])
            child = Student.objects.get(id=request.data["id"])
            serializer = ChildEditSerialierData(child, data=request.data)
            # address = int(request.data["address_details"])
            # # address = int(request.data["address_details"])
            # customer = int(request.data["customer"])

            print(serializer.is_valid())
            if serializer.is_valid():

                serializer.validated_data['first_name'] = request.data["first_name"]
                serializer.validated_data['last_name'] = request.data["last_name"]
                # serializer.validated_data['school_name'] = request.data["school_name"]
                # serializer.validated_data['address_details_id'] = address
                # serializer.validated_data['address_details_town'] = address
                # serializer.validated_data['customer_id'] = customer
                serializer.validated_data['birthdate'] = request.data["birthdate"]
                serializer.validated_data['medical_issue'] = request.data["medical_issue"]
                serializer.save()
                print("api saved")
            return JsonResponse({"message": "success"}, status=200)
        except Exception as e:
            print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ChildEditWithIdView(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            child = Student.objects.filter(id=pk)
            # print(id)
            serializers = ChildEditSerialier(child, many=True)

            return JsonResponse(serializers.data, safe=False)
        except Exception as e:

            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

    def post(self, request):

        try:
            json_data = request.data
            child_data = {"first_name": request.data["first_name"], "last_name": request.data["last_name"],
                          "birthdate": request.data["birthdate"], "medical_issue": request.data["medical_issue"]}
            # child = Student.objects.filter(id=pk)
            child = ChildEditSerialier(data=child_data)
            # print(child.is_valid())
            if child.is_valid():
                child.save()

                return JsonResponse(child.data, status=200)
            else:
                # print(child.errors)
                return JsonResponse(child.data, status=400)
        except Exception as e:
            # print("error", e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class StudentCourseGroupDataView(generics.GenericAPIView):
    """student details with group data using customer id"""

    def get(self, request, pk):
        try:

            customer = list(Customer.objects.filter(
                id=pk).values("id", "student", "student__ages"))
            print(customer)
            ages_data_for_student = []
            student_details = {'id': "", 'firstname': "", "lastname": "",
                               "dob": "", "age": "", "medical_issue": "", "coursedetail": ""}
            for student in customer:
                # print("student", student)
                for student_age_id in student:

                    if student_age_id == "student":

                        student_id = student[student_age_id]
                        child = list(Student.objects.filter(id=student_id, deleted=False).values(
                            "id", "ages_id", "ages__age", "first_name", "last_name", "birthdate", "medical_issue",))
                        # print(child)
                        student_details['id'] = child[0]["id"]
                        student_details['age'] = child[0]["ages__age"]
                        student_details['firstname'] = child[0]["first_name"]
                        student_details['lastname'] = child[0]["last_name"]
                        student_details['dob'] = child[0]["birthdate"]
                        student_details['medical_issue'] = child[0]["medical_issue"]

                        serializers = CourseGroupDataForStudentSerializer(
                            CourseGroupData.objects.filter(age=child[0]["ages_id"]), many=True)
                        student_details["coursedetail"] = serializers.data
                        print("course group", serializers.data)
                        ages_data_for_student.append(student_details)
                        # print(ages_data_for_student)
                        student_details = {'firstname': "", "lastname": "",
                                           "dob": "", "medical_issue": "", "coursedetail": []}

            return JsonResponse(ages_data_for_student, status=200, safe=False)
        except Exception as e:

            logger.error(e, exc_info=True)
            print(e)
            return render(request, '404-error-page.html')


class StudentCourseDetailData(generics.GenericAPIView):
    """student details with group data using customer id"""

    def get(self, request, pk, dk):
        try:

            customer = list(Customer.objects.filter(
                id=pk).values("id", "student", "student__ages"))

            ages_data_for_student = []
            temp_array = []
            student_details = {'id': "", 'firstname': "", "lastname": "",
                               "dob": "", "age": "", "medical_issue": "", "coursedetail": ""}
            for student in customer:
                # print("student", student)
                for student_age_id in student:

                    if student_age_id == "student":

                        student_id = student[student_age_id]
                        child = list(Student.objects.filter(id=student_id, deleted=False).values(
                            "id", "ages_id", "ages__age", "first_name", "last_name", "birthdate", "medical_issue",))
                        # print(child)
                        student_details['id'] = child[0]["id"]
                        student_details['age'] = child[0]["ages__age"]
                        student_details['firstname'] = child[0]["first_name"]
                        student_details['lastname'] = child[0]["last_name"]
                        student_details['dob'] = child[0]["birthdate"]
                        student_details['medical_issue'] = child[0]["medical_issue"]

                        serializers = CourseGroupDataForStudentSerializer(CourseGroupData.objects.filter(
                            age=child[0]["ages_id"], course_detail_id=dk), many=True)
                   

                        student_details["coursedetail"] = serializers.data

                        ages_data_for_student.append(student_details)

                        student_details = {'firstname': "", "lastname": "",
                                           "dob": "", "medical_issue": "", "coursedetail": []}
            for i in ages_data_for_student:

                if len(dict(i)["coursedetail"]) > 0:

                    temp_array.append(i)

            return JsonResponse(temp_array, status=200, safe=False)

        except Exception as e:

            logger.error(e, exc_info=True)
            print(e)
            return render(request, '404-error-page.html')


class CustomerStudentCount(generics.GenericAPIView):

    def get(self, request):
        try:
            total_student = Student.objects.all().count()
            total_customer = Customer.objects.all().count()
            count_data = [{
                "total_student": total_student,
                "total_customer": total_customer,
            }]
            return JsonResponse(count_data, status=200, safe=False)

        except Exception as e:
            logger.error(e)
            print(e)
            return render(request, '404-error-page.html')
