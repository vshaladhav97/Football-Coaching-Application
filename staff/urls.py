from django.urls import path
from .views import (StaffView, StaffListView, StaffEditView,
                    StaffDetailView, GetAllStaffView, StaffAddView,
                    SuperUserListView, GetAllSuperUserView, SuperUserView,
                    SuperUserAddView, SuperUserEditView, SuperUserDetailView)

urlpatterns = [
    #staff
    path('staff_list/', StaffListView.as_view(), name="staff_list"),
    path('get_all_staff/', GetAllStaffView.as_view(), name="get_all_staff"),
    path('staff/', StaffView.as_view(), name="staff"),
    path('staff_add/', StaffAddView.as_view(), name="staff_add"),
    path('staff_edit/<int:pk>', StaffEditView.as_view(), name="staff_edit"),
    path('staff/<int:pk>', StaffDetailView.as_view(), name="staff"),

    #super user
    path('super_user_list/', SuperUserListView.as_view(), name="super_user_list"),
    path('get_all_super_users/', GetAllSuperUserView.as_view(), name="get_all_super_users"),
    path('super_user/', SuperUserView.as_view(), name="super_user"),
    path('super_user_add/', SuperUserAddView.as_view(), name="super_user_add"),
    path('super_user_edit/<int:pk>', SuperUserEditView.as_view(), name="super_user_edit"),
    path('super_user/<int:pk>', SuperUserDetailView.as_view(), name="super_user"),
]