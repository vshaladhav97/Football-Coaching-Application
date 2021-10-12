from django.shortcuts import render
from rest_framework import generics, status
from django.http.response import HttpResponse, JsonResponse, Http404
from .serializer import LoginSerializer, LogoutSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from customer.models import User
from authentication.config import perms_config
from customer.views import get_permissions_wit_login
from customer.decorator import set_permission
from first_kick_management.settings import logger


# Create your views here.


class IndexView(generics.GenericAPIView):
    def get(self, request):
        """
        Get login page
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'index.html', {'login': login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Login using email and password
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            request.session['login'] = True
            request.session['email'] = request.data['email']
            set_permission(request, serializer.data['user'])
            user = User.objects.get(pk=serializer.data['user'])
            request.session['user'] = serializer.data['user']
            return JsonResponse({"message": "login successful", 'data': serializer.data, "role": user.role.name}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def get(self, request):
        """
        Get login page
        """
        try:
            return render(request, 'login-and-register.html', {})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class LogOutView(generics.GenericAPIView):
    # serializer_class = LogoutSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Clear everything on log out
        """
        try:
            # serializer = self.serializer_class(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            request.session.flush()
            return JsonResponse({"message": "log out successful"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return JsonResponse({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return JsonResponse({'message': 'Password updated successfully'}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
