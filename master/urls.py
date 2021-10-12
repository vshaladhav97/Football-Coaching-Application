from django.urls import path
from .views import (LocationView, AgeGroupView, EventTypeView, AgesView, PlayingSurfaceView,
                    CourseTypeView, MonthView, LocationPageView, LocationEditView,
                    LocationDetailView, LocationAddView, ClassStatusView, GetAllLocationView,
                    CourseTypeDetailView, AgesByIdView, AddressDetailsForPrepopulationView, CourseTypeForDropdownView,
                    CompanyNameDropdownSelectionView)

urlpatterns = [
    path('location_list/', LocationPageView.as_view(), name="location_list"),
    path('get_all_locations/', GetAllLocationView.as_view(),
         name="get_all_locations"),
    path('locations/', LocationView.as_view(), name="location"),
    path('locations/<int:pk>', LocationDetailView.as_view(), name="location_detail"),
    path('location_add/', LocationAddView.as_view(), name="location_add"),
    path('location_edit/<int:pk>', LocationEditView.as_view(), name="location_edit"),
    path('age_group/', AgeGroupView.as_view(), name="age_group"),
    path('course_type/', CourseTypeView.as_view(), name="course_type"),
    path('course_type_for_dropdown/', CourseTypeForDropdownView.as_view(), name="course_type_for_dropdown"),
    path('course_type/<int:pk>', CourseTypeDetailView.as_view(),
         name="course_type_detail"),
    path('event_type/', EventTypeView.as_view(), name="event_type"),
    path('class_status/', ClassStatusView.as_view(), name="class_status"),
    path('months/', MonthView.as_view(), name="months"),
    path('ages/', AgesView.as_view(), name="ages"),
    path('ages/<int:pk>', AgesByIdView.as_view(), name="ages"),
    path('playing_surface/', PlayingSurfaceView.as_view(), name="playing_surface"),
    path('address_details_for_prepolation/', AddressDetailsForPrepopulationView.as_view(), name="address_details_for_prepolation"),
    path('company_dropdown_list/', CompanyNameDropdownSelectionView.as_view(), name="company_dropdown_list"),
]
