from django.shortcuts import render
from ..models import (CourseType, EventType)
from rest_framework import generics
from django.http.response import JsonResponse
from ..serializer import (EvenTypeSerializer,CourseTypeSerializer)
from first_kick_management.settings import logger


class CourseTypeView(generics.GenericAPIView):
    serializer_class = CourseTypeSerializer

    def get(self, request):
        """
        Get all course type
        """
        try:
            serializer = CourseTypeSerializer(CourseType.objects.all(), many=True)
            return JsonResponse({"message": "course type list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class CourseTypeForDropdownView(generics.GenericAPIView):
    serializer_class = CourseTypeSerializer

    def get(self, request):
        """
        Get all course type
        """
        try:
            serializer = CourseTypeSerializer(CourseType.objects.exclude(course_name="Parties"), many=True)
            return JsonResponse({"message": "course type list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CourseTypeDetailView(generics.GenericAPIView):
    serializer_class = CourseTypeSerializer

    def get(self, request, pk):
        """
        Get course type detail
        """
        try:
            serializer = CourseTypeSerializer(CourseType.objects.get(pk=pk))
            return JsonResponse({"message": "course type detail", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class EventTypeView(generics.GenericAPIView):
    serializer_class = EvenTypeSerializer

    def get(self, request):
        """
        Get all event types
        """
        try:
            serializer = EvenTypeSerializer(EventType.objects.all(), many=True)
            return JsonResponse({"message": "event type list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)