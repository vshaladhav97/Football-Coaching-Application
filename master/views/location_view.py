import json
from django.db.models.query_utils import select_related_descend
from django.shortcuts import render
from ..models import (AddressDetail, Company, Location, CourseWiseSuitableLocation,
                      PlayingSurface, query_location_by_args)
from master.models import CourseType
from rest_framework import generics
from django.http.response import HttpResponse, JsonResponse, Http404
from ..serializer import (LocationSerializer, LocationDataTableSerializer,
                          PlayingSurfaceSerializer, LocationDataTableSerializerForPrepolated, AddressDetailSerializer,
                          CompanyNameDropdownSelectionSerializer)
from rest_framework.response import Response
from first_kick_management.settings import logger
# import requests


class Error(Exception):
    """Base class for other exceptions"""
    pass


class CompanyExistError(Error):
    pass


class LocationPageView(generics.GenericAPIView):
    def get(self, request):
        try:
            login = True if "login" in request.session else False
            return render(request, 'location/location_list.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class LocationAddView(generics.GenericAPIView):

    def get(self, request):
        """
        Gwt student list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'location/location_add.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class LocationEditView(generics.GenericAPIView):

    def get(self, request, pk):
        """
        Gwt student list view
        """
        try:
            login = True if "login" in request.session else False
            return render(request, 'location/location_edit.html', {"login": login})
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')


class GetAllLocationView(generics.GenericAPIView):
    serializer_class = LocationDataTableSerializer

    def get(self, request):
        """
        Get all event types
        """
        try:
            serializer = LocationDataTableSerializer(
                Location.objects.all(), many=True)
            return JsonResponse({"message": "location list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class LocationView(generics.GenericAPIView):
    serializer_class = LocationDataTableSerializer

    def get(self, request):
        """
        Get all location
        """
        try:
            print(request.data)
            datatable_server_processing = query_location_by_args(
                request, **request.query_params)
            serializer = LocationDataTableSerializer(
                datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
            # serializer = AddressDetailSerializer(AddressDetail.objects.all().values('town','id').distinct(), many=True)
            # return JsonResponse({"message": "location list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Create company
        """
        try:

            json_data = request.data
            print(json_data)
            # print(json_data['company_name'].isnumeric())
            if json_data['company_name'].isnumeric():
                company = request.POST.getlist('company_name')
            else:
                print("hello")
                company = Location.objects.filter(
                    location__iexact=request.data['company']).exists()
                if company:
                    raise CompanyExistError
                company_obj = Company.objects.create(
                    company_name=request.data['company'])
            course_types = list()
            venue_name = request.POST.getlist('venue_name')
            street = request.POST.getlist('street')
            town = request.POST.getlist('town')
            post_code = request.POST.getlist('post_code')
            playing_surface = request.POST.getlist('playing_surface')
            course_types_1 = request.POST.getlist('course_type[1]')
            course_types_2 = request.POST.getlist('course_type[2]')
            course_types.append(course_types_1)
            course_types.append(course_types_2)

            for key in range(0, len(venue_name)):
                if json_data['company_name'].isnumeric():

                    location = Location.objects.create(
                        company=Company.objects.get(
                            pk=company[key]),
                        location=venue_name[key],
                        town=town[key],
                        postal_code=post_code[key],
                        address_line_1=street[key],
                        playing_surface=PlayingSurface.objects.get(
                            pk=playing_surface[key])
                    )
                else:
                    location = Location.objects.create(
                        company=company_obj,
                        location=venue_name[key],
                        town=town[key],
                        postal_code=post_code[key],
                        address_line_1=street[key],
                        playing_surface=PlayingSurface.objects.get(
                            pk=playing_surface[key])
                    )

                for item in course_types[key]:
                    CourseWiseSuitableLocation.objects.create(
                        location=location,
                        course_type=CourseType.objects.get(pk=item)
                    )
            return JsonResponse({"message": "created successfully"}, status=200)
        except CompanyExistError:
            return JsonResponse({'message': "company already exist"})
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


# class SaveLocationWithCompanyIdOrCompanyNameView(generics.GenericAPIView):
#     """Save company name or company id view for location """

#     def post(self, request):
#         try:
#             json_data = request.data
#             data = "first_name": request.data["first_name"]
#             serializer = 

class AddressDetailsForPrepopulationView(generics.GenericAPIView):

    def get(self, request):
        try:
            address = AddressDetail.objects.all()
            serializer = AddressDetailSerializer(address, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except Exception as e:
            print(e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class LocationDetailView(generics.GenericAPIView):
    serializer_class = LocationDataTableSerializer

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            location = self.get_object(pk)
            serializer = LocationDataTableSerializerForPrepolated(location)
            return JsonResponse({'message': 'get location details', 'data': serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def put(self, request, pk):
        """
        Update student
        """
        try:
            location = self.get_object(pk)
            print('loaction', location)
            print('req ', request.data)
            serializer = LocationDataTableSerializer(
                location, data=request.data)
            if serializer.is_valid():
                print('inside if')
                serializer.save()
                return JsonResponse({'message': 'update location', 'data': serializer.data}, status=200)
            return Response(serializer.errors)
        except Exception as e:
            logger.error(e, exc_info=True)
            print(e)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def delete(self, request, pk):
        """
        Delete buyer
        """
        try:
            location = self.get_object(pk)
            if location:
                location.delete()
                return JsonResponse({'message': "Location deleted successfully"}, status=200)
            return JsonResponse({'message': "Location not found"}, status=401)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class PlayingSurfaceView(generics.GenericAPIView):
    serializer_class = PlayingSurfaceSerializer

    def get(self, request):
        """
        Get all ages
        """
        try:
            serializer = PlayingSurfaceSerializer(
                PlayingSurface.objects.all(), many=True)
            return JsonResponse({"message": "surface list", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

class CompanyNameDropdownSelectionView(generics.GenericAPIView):
    """Company Names For DropDown View"""
    def get(self, request):

        try:
            company_name = Company.objects.all()
            serializer = CompanyNameDropdownSelectionSerializer(company_name, many = True)
            return JsonResponse(serializer.data, status = 200, safe=False)
        except Exception as e:
            print(e)
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

        


