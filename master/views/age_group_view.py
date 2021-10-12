from django.shortcuts import render
from ..models import (AddressDetail, Location, AgeGroup, Ages)
from rest_framework import generics
from django.http.response import HttpResponse, JsonResponse, Http404
from ..serializer import (LocationSerializer, AgeGroupSerializer, AgeSerializer)
from first_kick_management.settings import logger


class Error(Exception):
    """Base class for other exceptions"""
    pass


class AgeGroupExistError(Error):
    pass


class AgeGroupView(generics.GenericAPIView):
    serializer_class = AgeGroupSerializer

    def get(self, request):
        """
        Get all customers
        """
        try:
            serializer = AgeGroupSerializer(AgeGroup.objects.all(), many=True)
            return JsonResponse({"message": "age group list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Create customer
        """
        try:

            location = Location.objects.filter(location__iexact=request.data['location']).exists()
            if location:
                raise AgeGroupExistError

            request.data._mutable = False
            location_serializer = LocationSerializer(data=request.data)
            if location_serializer.is_valid(
                    raise_exception=True):

                address_detail = AddressDetail.objects.create(
                    address_line_1=request.data['address_line_1'],
                    address_line_2=request.data['address_line_2'],
                    address_line_3=request.data['address_line_3'],
                    town=request.data['town'],
                    country=request.data['country'],
                    postal_code=request.data['postal_code'],
                )

                location = Location.objects.create(
                    location=request.data['location'],
                    address_detail=address_detail,
                )

                return JsonResponse({"message": "created successfully"}, status=200)

        except AgeGroupExistError:
            return JsonResponse({'message': "age group already exist"})

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class AgesView(generics.GenericAPIView):
    serializer_class = AgeSerializer

    def get(self, request):
        """
        Get all ages
        """
        try:
            serializer = AgeSerializer(Ages.objects.all(), many=True)

            return JsonResponse({"message": "age list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class AgesByIdView(generics.GenericAPIView):
    serializer_class = AgeSerializer

    def get(self, request, pk):
        """
        Get all ages
        """
        try:
            serializer1 = AgeSerializer(Ages.objects.filter(coursetype__id=pk), many=True)
            serializer2 = AgeSerializer(Ages.objects.all(), many=True)
            array1 = list(map(lambda x : x['age'], serializer1.data))
            array2 = list(map(lambda x : x['age'], serializer2.data))
            array3 = list(map(lambda x : x['id'], serializer2.data))
            final_list = []
            for i in range(len(array2)):
                final_dict = {}
                final_dict['age'] = array2[i]
                final_dict['id'] = array3[i]
                if array2[i] in array1:
                    final_dict['checked'] = True
                else:
                    final_dict['checked'] = False
                final_list.append(final_dict)

            
            return JsonResponse({"message": "age list", "data": final_list}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            # print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)