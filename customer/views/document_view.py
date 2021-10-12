from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from ..models import Customer, User, Student, Role, query_users_by_args, query_students_by_args, CustomerDocuments
from coach.models import Coach, CoachDocuments
from coach.serializer import CoachDocumentSerializer
from customer.serializer import CustomerDocumentSerializer
from customer.decorator import check_role_permission
from first_kick_management.settings import logger


class DocumentView(generics.GenericAPIView):
    @check_role_permission()
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'user/document.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class GetAllDocuments(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            serializer = None
            role = str(request.user.role)
            if role == "Customer":
                serializer = CustomerDocumentSerializer(
                    CustomerDocuments.objects.filter(
                        customer=Customer.objects.get(email__iexact=request.user.email)), many=True)
            if role == "Coach Manager" or role == "Head Coach":
                serializer = CoachDocumentSerializer(
                    CoachDocuments.objects.filter(
                        coach=Coach.objects.get(email__iexact=request.user.email)), many=True)

            return JsonResponse({'message': 'list of all documents', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)