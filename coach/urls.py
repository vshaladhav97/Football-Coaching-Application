from django.urls import path
from .views import (CoachView, CoachListView, CoachEditView,
                    CoachDetailView, GetAllCoachView, CoachAddView,
                    VenueAnalytics, ClassRegisterView, RotaView, RotaDataView, VenueAnalyticsCountView, 
                    CoachAnalyticsListView, VenueAnalyticsListView, DynamicVenueAnalyticsCountView, testingrota)

urlpatterns = [
    path('coach_list/', CoachListView.as_view(), name="coach_list"),
    path('get_all_coach/', GetAllCoachView.as_view(), name="get_all_coach"),
    path('coach/', CoachView.as_view(), name="coach"),
    path('coach_add/', CoachAddView.as_view(), name="coach_add"),
    path('coach_edit/<int:pk>', CoachEditView.as_view(), name="coach_edit"),
    path('coach/<int:pk>', CoachDetailView.as_view(), name="coach_detail"),
    path('venue_analytics/', VenueAnalytics.as_view(), name="venue_analytics"),
    path('rota/', RotaView.as_view(), name="rota"),
    path('rota_data/', RotaDataView.as_view(), name="rota_data"),
    path('rota_data/<order_by>', RotaDataView.as_view(), name="rota_data"),
    path('venue_analytics_count/', VenueAnalyticsCountView.as_view(), name="venue_analytics_count"),
    path('venue_analytics_count/<int:pk>', DynamicVenueAnalyticsCountView.as_view(), name="dynamic_venue_coach_count"),
    path('coach_list_analytics/', CoachAnalyticsListView.as_view(), name="coach_list_analytics"),
    path('venue_list_analytics/', VenueAnalyticsListView.as_view(), name="venue_list_analytics"),
    # path('class_register/', ClassRegisterView.as_view(), name="class_register"),
    path('test_rota/', testingrota.as_view()),
]