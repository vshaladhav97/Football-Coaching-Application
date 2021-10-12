from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse, Http404
from rest_framework.permissions import IsAuthenticated
from actstream.models import Action
from ..serializer import RecentActivitySerializer
from first_kick_management.settings import logger
import json


class RecentActivitiesView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get cart items
        """
        try:
            data = request.user.role.name
            data1 = request.user.role
            if request.user.role.name == "Head Coach":
                serializer = RecentActivitySerializer(Action.objects.filter(target_object_id=request.user.id)[:10], many=True)
            else:
                serializer = RecentActivitySerializer(Action.objects.filter()[:10], many=True)

            return JsonResponse({"message": "list of recent activities", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


