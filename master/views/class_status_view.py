from django.shortcuts import render
from ..models import (ClassStatus)
from rest_framework import generics
from django.http.response import JsonResponse
from ..serializer import (ClassStatusSerializer)
from first_kick_management.settings import logger
# Create your views here.


class ClassStatusView(generics.GenericAPIView):
    serializer_class = ClassStatusSerializer

    def get(self, request):
        """
        Get all event types
        """
        try:
            serializer = ClassStatusSerializer(ClassStatus.objects.all(), many=True)
            return JsonResponse({"message": "class status list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)