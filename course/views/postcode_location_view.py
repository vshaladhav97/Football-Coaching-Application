from ..models import (CourseDetail)
from django.http.response import JsonResponse
from rest_framework import generics
from .postcode import call_distance_matrix, sort_list_of_location, validate_postcode
import json
from first_kick_management.settings import logger



class GetDistanceByPostCode(generics.GenericAPIView):

    """Get distance between search postcode and database postcode"""

    def post(self, request):
        try:
            # print(request.data)
            data = request.data
            if 'postcode' not in data and 'course_type_id' not in data:
                return JsonResponse({"message": "Please send data having both postcode and course_type_id"}, status=422)
            
            origins = data['postcode']
            if not validate_postcode(origins):
                return JsonResponse({"message": "Please Enter Valid Postcode"}, status=400)
                
            course_type_id = data['course_type_id']
            distance_list = []
            data_base_locations = list(CourseDetail.objects.filter(course_type__id=course_type_id).values("location", "location__location",
                                                                                                          "location__address_line_1","location__town", "location__postal_code", "location__country",))
            # print(len(data_base_locations))
            list_of_locations = []
            start = 0

            for i in range(len(data_base_locations)):
                end = start
                start += 25

                if len(data_base_locations[end:start]) == 0:
                    break
                else:
                    list_of_locations.append(data_base_locations[end:start])

            for locations in list_of_locations:
                destinations = '|'.join(
                    ["".join(d['location__postal_code'].split()) for d in locations])

                response = call_distance_matrix(origins, destinations)

                if response.status_code == 200:
                    content = json.loads(response.content)
                    elements = content['rows'][0]['elements']

                    for data_index in range(len(elements)):
                        """Iterate the resultant distance and database location elements to format the json"""

                        if elements[data_index]['status'] == 'OK':
                            """Check the status of the postcode"""

                            distance = elements[data_index]['distance']['text']

                            if float(distance.split(' ')[0]) <= 50:
                                """Check the radius of the mile"""

                                distance_dict = {}
                                distance_dict['distance'] = distance
                                distance_dict['location_id'] = locations[data_index]['location']
                                distance_dict['location'] = locations[data_index]['location__location']
                                distance_dict['address'] = locations[data_index]['location__address_line_1']
                                distance_dict['town'] = locations[data_index]['location__town']
                                distance_dict['postal_code'] = locations[data_index]['location__postal_code']
                                distance_dict['country'] = locations[data_index]['location__country']
                                distance_list.append(distance_dict)
                else:
                    return JsonResponse({"message": "Something went wrong, please contact admin"}, status=response.status_code)
            result = sort_list_of_location(distance_list)
            return JsonResponse({"message": result[:4]}, status=200)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
