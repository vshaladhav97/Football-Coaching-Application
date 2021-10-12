from django.shortcuts import render
from ..models import (Months, WeekDay)
from rest_framework import generics
from django.http.response import JsonResponse
from ..serializer import (WeekDaySerializer,MonthSerializer)
from first_kick_management.settings import logger

# Create your views here.


class WeekDayView(generics.GenericAPIView):
    serializer_class = WeekDaySerializer

    def get(self, request):
        """
        Get all weekdays
        """
        try:
            serializer = WeekDaySerializer(WeekDay.objects.all(), many=True)
            return JsonResponse({"message": "week day list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class MonthView(generics.GenericAPIView):
    serializer_class = MonthSerializer

    def get(self, request):
        """
        Get all weekdays
        """
        try:
            serializer = MonthSerializer(Months.objects.all(), many=True)
            return JsonResponse({"message": "months list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
