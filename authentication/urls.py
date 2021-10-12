from django.urls import path

from .views import (LoginView, LogOutView, IndexView, ChangePasswordView)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
     path('', IndexView.as_view(), name="index"),
     path('login/', LoginView.as_view(), name="login"),
     path('logout/', LogOutView.as_view(), name="logout"),
     path('change_password/', ChangePasswordView.as_view(), name="change_password"),
     # path('access/',
     #     jwt_views.TokenObtainPairView.as_view(),
     #     name='token_obtain_pair'),
     path('refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]